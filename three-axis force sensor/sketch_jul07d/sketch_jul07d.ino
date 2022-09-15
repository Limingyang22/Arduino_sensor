#include <SoftwareSerial.h>
unsigned char item[8] = {0x01, 0x03, 0x01, 0x00, 0x00, 0x06, 0xc4, 0x34};  //16进制命令
//char data = ""; // 接收到的16进制字符串

void setup()
{
  Serial1.begin(9600);
  Serial2.begin(9600);
}

void loop()
{
  delay(800);  // 放慢输出频率
  for (int i = 0 ; i < 8; i++) {  // 发送命令
    Serial2.write(item[i]);   // write输出
  }
  delay(150);  // 等待数据返回
  while (Serial1.available()) {//从串口中读取数据
    String in = Serial1.readString();  
    Serial1.print(in);  // read读取
   // delay(20);
  }
}
