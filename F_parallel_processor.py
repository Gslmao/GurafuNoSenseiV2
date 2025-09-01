from multiprocessing import Queue, Process
from F_eqn_processor import MainApp
from dotenv import load_dotenv

import matplotlib.pyplot as plt
import pickle
import os

load_dotenv()

class Helper:
    def __init__(self):
        
        self.directory = os.getenv("FILES_PATH")

    def eqns_state(self):
        file_path = os.path.join(self.directory, "my_file.dat")
        with open(file_path, 'rb') as file:
            det = pickle.load(file)
        eqns = det['eqns']
        savestate = det['savestate']
        operator = det['calc']

        if len(det['limits']) != 0:
            limits = det['limits']
        else:
            limits = []
        return eqns, savestate, operator, limits

class MultiProcessor:
    def __init__(self):
        self.process = Helper()
        self.processes = []
        self.queue = Queue()

    def main(self):
        eqns, savestate, operator, limits = self.process.eqns_state()
        eqns = [eqn.strip() for eqn in eqns if eqn != ""]

        for eqn in eqns:
            if eqn != "":
                prc = Process(target=MultiProcessor.worker, args=(eqn, savestate, self.queue, operator, limits))
                self.processes.append(prc)
                prc.start()

        results = [self.queue.get() for _ in range(len(self.processes))]
        results = [r for r in results if r is not None]
        fig, ax = self.plotstuff(results, operator, limits)

        file_path = os.path.join(self.process.directory, "fig_file.pkl")
        with open(file_path, 'wb') as file:
            pickle.dump(fig, file)

    @staticmethod
    def worker(eqn, state, queue, f, limits):
        instance = MainApp(eqn, operator=f, limits=limits)

        result, equation = instance.plot_eqn(eqn)
        queue.put((result, equation, f))

    @staticmethod
    def plotstuff(results, global_operator, limits):
        limits = limits
        fig, ax = plt.subplots(figsize=(6.5, 5.5))

        for coord, equation, operator in results:
            if coord and len(coord) >= 2:
                ax.plot(coord['x'], coord['y'], label=f'{equation}')

                if operator == 'd' and global_operator == 'd':
                    ax.plot(coord['x'], coord['deriv'], label=f'Derivative of {equation}')

                elif operator == 'i' and global_operator == 'i':
                    ax.plot(coord['x'], coord['int_inf'], label=f'Integral of {equation}')

                    if limits[0] == 0 and limits[1] == 0:
                        pass
                    else:
                        ax.fill_between(coord['sh_x'], coord['sh_y'], color='green', alpha=0.3)

        ax.set_xlabel("X Axis")
        ax.set_ylabel("Y Axis")
        ax.grid()
        ax.legend()
        ax.axvline(0, color="black")
        ax.axhline(0, color="black")

        return fig, ax

if __name__ == "__main__":
    processor = MultiProcessor()
    processor.main()
