# Touch 上位机工具





## 使用方法

1. 请先安装好python程序需要的第三方依赖包。
2. 使用对应的下位机程序和硬件进行测试。
3. 修改`TouchConfiguration.json`文件中**`串口号：port`**
   - 下位机使用`UART2`
   - 波特率：`500000`
4. 建议使用window系统的`cmd/powershell`打开该python上位机程序，方便检查log信息。
5. 先运行python程序，之后再给下位机板子上电。
6. view 输出内容。

| 文件输出     | 作用                                  |
| ------------ | ------------------------------------- |
| fine.csv     | 用于保存程序运行期间，Touch原始数据   |
| baseline.csv | 用于保存程序运行期间，Touch基线值数据 |
|              |                                       |



## 注意事项

1. 上位机程序中，因为未加入纠错机制，因此一旦UART传输发生错误，上位机程序将会停止运行。
2. python程序运行过程中，不要打开csv文件，会打断程序运行。
3. 使用CTRL+C打断python程序运行。
4. python版本要求：3.X以上。



## 第三方包依赖

1. pip install serial
2. pip install crccheck



## 更新记录

### Rev1.1

- 2021.04.16
  - 输出Touch数据到`csv`文件

