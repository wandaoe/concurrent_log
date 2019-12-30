# concurrent_log
支持多进程多线程环境使用的日志处理器

## ConcurrentTimedRotatingFileHandler

### 支持的功能
1. 按照时间进行切割日志  
1. 支持多进程多线程环境使用

### 怎么用  
与标准库`TimedRotatingFileHandler`完全兼容。  
如果项目已经使用了`TimedRotatingFileHandler`，来进行日志处理，因为引入了多进程机制需要一个支持多进程环境的日志处理器，只需要在
日志配置界面引入`concurrent_log`模块，然后将`TimedRotatingFileHandler`替换为`ConcurrentTimedRotatingFileHandler`即
可，其他代码不需要任何改动。

### 压测示例代码
```python
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

class ConcurrentTimedRotatingFileHandlerTest:
    """
    ConcurrentTimedRotatingFileHandler 测试
    """

    def __init__(self):
        import logging
        import logging.config

        import concurrent_log

        log_conf = {
            'version': 1,
            'formatters': {
                'default': {
                    'format': '%(asctime)s - %(process)d-%(threadName)s - '
                              '%(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    'datefmt': "%Y-%m-%d %H:%M:%S"
                },
            },
            'handlers': {
                'file': {
                    'level': 'DEBUG',
                    'class': 'logging.handlers.ConcurrentTimedRotatingFileHandler',
                    'backupCount': 100,
                    'when': 's',
                    'delay': True,
                    'filename': 'log/test.log',
                    'encoding': 'utf-8',
                    'formatter': 'default',
                }
            },
            'root': {
                'handlers': ['file'],
                'level': 'DEBUG',
            },
        }

        logging.config.dictConfig(log_conf)
        self.logger = logging.getLogger(__name__)

    def write_log(self, index):
        self.logger.debug('debug-%s' % index)
        self.logger.info('info-%s' % index)
        self.logger.warning('警告-%s' % index)
        self.logger.error('报错-%s' % index)
        self.logger.critical('严重-%s' % index)

    def mutil_thread_write_log(self):
        with ThreadPoolExecutor(100) as thread_pool:
            for i in range(1000):
                thread_pool.submit(self.write_log, i).add_done_callback(self._executor_callback)

    def mutil_process_write_log(self):
        with ProcessPoolExecutor() as process_pool:
            for i in range(100):
                process_pool.submit(self.mutil_thread_write_log).add_done_callback(self._executor_callback)

    def _executor_callback(self, worker):
        worker_exception = worker.exception()
        if worker_exception:
            print("Worker return exception: ", self.worker_exception)


class TimedRotatingFileHandlerTest:
    """
    TimedRotatingFileHandler 测试
    """

    def __init__(self):
        import logging
        import logging.config

        log_conf = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'default': {
                    'format': '%(asctime)s - %(process)d-%(threadName)s - '
                              '%(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    'datefmt': "%Y-%m-%d %H:%M:%S"
                },
            },
            'handlers': {
                'file': {
                    'level': 'DEBUG',
                    'class': 'logging.handlers.TimedRotatingFileHandler',
                    'backupCount': 100,
                    'when': 's',
                    'delay': True,
                    'filename': 'log2/test.log',
                    'encoding': 'utf-8',
                    'formatter': 'default',
                }
            },
            'root': {
                'handlers': ['file'],
                'level': 'DEBUG',
            },
        }

        import os
        file_path = os.path.split(log_conf.get("handlers").get("file").get("filename"))[0]
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        logging.config.dictConfig(log_conf)
        self.logger = logging.getLogger(__name__)

    def write_log(self, index):
        self.logger.debug('debug-%s' % index)
        self.logger.info('info-%s' % index)
        self.logger.warning('警告-%s' % index)
        self.logger.error('报错-%s' % index)
        self.logger.critical('严重-%s' % index)

    def mutil_thread_write_log(self):
        with ThreadPoolExecutor(100) as thread_pool:
            for i in range(100000):
                thread_pool.submit(self.write_log, i).add_done_callback(self._executor_callback)

    def _executor_callback(self, worker):
        worker_exception = worker.exception()
        if worker_exception:
            print("Worker return exception: ", self.worker_exception)


if __name__ == "__main__":
    print("50W日志写入测试")
    begin_time = time.time()
    # 多进程写入日志，进程数与CPU核心数一致，使用文件锁实现进程并发控制，防止脏数据以及日志丢失
    # 每个进程100个线程共需写入五千行日志，由于GIL原因，并发只存在一个线程，但是会存在线程上下文切换，使用线程锁防止脏数据和日志丢失
    ConcurrentTimedRotatingFileHandlerTest().mutil_process_write_log()
    use_time = time.time() - begin_time
    print("ConcurrentTimedRotatingFileHandler 耗时:%s秒" % use_time)
    begin_time = time.time()
    # 每个进程100个线程共需写入所有日志，由于GIL原因，并发只存在一个线程，但是会存在线程上下文切换，同样需要锁机制防止脏数据和日志丢失
    TimedRotatingFileHandlerTest().mutil_thread_write_log()
    use_time = time.time() - begin_time
    print("TimedRotatingFileHandler 耗时:%s秒" % use_time)
```

### 压测结果
经验证，日志内容完整，按照时间切割正确  

**环境**  
CPU：Intel® Core™ i9-7940X  
内存：64G  
磁盘：三星 970Pro 1T  

**输出**  
50W日志写入测试  
ConcurrentTimedRotatingFileHandler 耗时:84.82415437698364秒  
TimedRotatingFileHandler 耗时:100.73775053024292秒  
