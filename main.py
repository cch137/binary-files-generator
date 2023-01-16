import random, sys, shutil, os, threading, math, time


T0 = time.time()
CONTENT_IS_RANDOM = False
OUTPUT_PATH = 'output/'
shutil.rmtree(OUTPUT_PATH, ignore_errors=True)
os.mkdir(OUTPUT_PATH)

targetSize = 15 * 1042 * 1024 * 1024 # 15GB
splitSize = 1024 * 1024 # 1MB

sys.set_int_max_str_digits(splitSize + 1024)

class generateThread(threading.Thread):
  def __init__(self, filepath: str, filesize: int) -> None:
    threading.Thread.__init__(self)
    self.filepath = filepath
    self.filesize = filesize
    self.done = False
  def run(self) -> None:
    try:
      with open(self.filepath, 'wb') as f:
        if CONTENT_IS_RANDOM: binaryInt = [i for i in random.choices('01', k=self.filesize)]
        else: binaryInt = '1' * filesize
        if binaryInt[0] == '0': binaryInt[0] = '1'
        binaryInt = int(''.join(binaryInt), 2)
        f.write(binaryInt.to_bytes(binaryInt.bit_length(), byteorder='big'))
    except Exception as err:
      print(err)
    self.done = True

threads = []
fileNumber = 1

class statusThread(threading.Thread):
  def __init__(self) -> None:
    threading.Thread.__init__(self)
    pass
  def run(self) -> None:
    totalFileAmounts = len(threads)
    print(f'There are {totalFileAmounts} files to be generated.')
    doneThreadsAmount = 0
    while doneThreadsAmount < totalFileAmounts:
      doneThreadsAmount = len([1 for t in threads if t.done])
      print(f'Processing... {round(100 * doneThreadsAmount / totalFileAmounts, 2)}% ({doneThreadsAmount}/{totalFileAmounts})')
      time.sleep(5)

status = statusThread()
status.start()

while targetSize > 0:
  filesize = min(targetSize, splitSize)
  targetSize -= splitSize
  threads.append(generateThread(f'{OUTPUT_PATH}{"{:08d}".format(fileNumber)}.temp', filesize))
  fileNumber += 1
for t in threads: t.start()
for t in threads: t.join()
print(f'Time used: {round(time.time() - T0, 4)}s')
input('Press ENTER to continue...')