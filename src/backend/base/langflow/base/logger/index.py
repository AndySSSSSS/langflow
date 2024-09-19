import logging
from logging.handlers import TimedRotatingFileHandler
import os
import concurrent.futures
from threading import Lock


class AsyncLogger:
    _instance = None  # 用于保存单例实例
    _lock = Lock()    # 确保线程安全

    def __init__(self, log_dir="./logs", log_file_name="ai.log", backup_count=7, level=logging.INFO):
        """
        初始化异步日志记录器，只能通过 get_instance 方法获取实例。
        """
        if not hasattr(self, "_initialized"):  # 防止重复初始化
            self._initialized = True
            self.log_dir = log_dir
            self.log_file_name = log_file_name
            self.backup_count = backup_count
            self.level = level

            # 初始化日志记录器
            self.logger = self._setup_logger()

            # 创建线程池执行器用于异步输出
            self.executor = concurrent.futures.ThreadPoolExecutor()

    @classmethod
    def get_instance(cls):
        """
        获取单例实例，确保全局唯一。
        """
        if cls._instance is None:
            with cls._lock:  # 确保线程安全的单例创建
                if cls._instance is None:
                    cls._instance = cls()  # 创建单例实例
        return cls._instance

    def _setup_logger(self):
        """
        初始化日志记录器并设置处理器
        :return: 日志记录器对象
        """
        # 确保日志目录存在
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        # 日志文件路径
        log_file_path = os.path.join(self.log_dir, self.log_file_name)

        # 创建日志记录器
        logger = logging.getLogger(self.log_file_name)
        logger.setLevel(self.level)

        # 防止重复添加 handler
        if not logger.handlers:
            # 创建一个按日期分割的处理器，文件每天分割一次
            handler = TimedRotatingFileHandler(log_file_path, when="midnight", interval=1, backupCount=self.backup_count)
            handler.suffix = "%Y-%m-%d"  # 定义日志文件名的日期后缀

            # 创建日志格式
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)

            # 将处理器添加到日志记录器
            logger.addHandler(handler)

        return logger

    @staticmethod
    def log(message, level=logging.INFO):
        """
        静态方法：异步记录日志信息
        :param message: 要记录的日志消息
        :param level: 日志级别，默认INFO
        """
        logger_instance = AsyncLogger.get_instance()  # 获取单例实例
        # 提交到线程池，异步执行
        logger_instance.executor.submit(logger_instance._log_message, message, level)

    def _log_message(self, message, level):
        """
        内部方法，记录日志消息
        :param message: 要记录的日志消息
        :param level: 日志级别
        """
        if level == logging.DEBUG:
            self.logger.debug(message)
        elif level == logging.WARNING:
            self.logger.warning(message)
        elif level == logging.ERROR:
            self.logger.error(message)
        elif level == logging.CRITICAL:
            self.logger.critical(message)
        else:
            self.logger.info(message)

    @staticmethod
    def shutdown():
        """
        静态方法：关闭线程池执行器和日志处理器
        """
        logger_instance = AsyncLogger.get_instance()  # 获取单例实例
        logger_instance.executor.shutdown()
        logging.shutdown()


# 示例用法
if __name__ == "__main__":
    # 不需要显式创建实例，可以直接调用静态方法记录日志
    AsyncLogger.log("This is an info message.")
    AsyncLogger.log("This is an error message.", level=logging.ERROR)

    # 程序结束时关闭日志
    AsyncLogger.shutdown()
