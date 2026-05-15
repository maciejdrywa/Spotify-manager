from PyQt6.QtCore import QThread, QObject

class WorkerController(QObject):
    def __init__(self):
        super().__init__()

        self._active_tasks = []


    def _start_worker(self, worker, on_finished, on_error=None):
        thread = QThread()

        worker.moveToThread(thread)

        thread.started.connect(worker.run)

        worker.finished.connect(on_finished)

        if on_error is None:
            worker.error.connect(self._on_worker_error)
        else:
            worker.error.connect(on_error)

        worker.finished.connect(thread.quit)
        worker.error.connect(thread.quit)

        worker.finished.connect(worker.deleteLater)
        worker.error.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)

        task = {
            "thread": thread,
            "worker": worker
        }

        self._active_tasks.append(task)

        thread.finished.connect(lambda: self._active_tasks.remove(task))

        thread.start()

        
    def _on_worker_error(self, message):
        print(f"Worker error: {message}")


        