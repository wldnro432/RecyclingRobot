#include <WiFi.h>
#include <ESP32Servo.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
Servo servo1;
Servo servo2;
Servo servo4;
Servo servo5;

const char *ssid = "ANE_Class2_2G";
const char *password = "addinedu_class2@";
int i = 60;
char input = 'k';
int e;
int del = 70;
const char html[] PROGMEM = R"rawliteral(
<!DOCTYPE html>
<html>
<body>
<center>
<style>
body { background-color: lightblue; }
</style>
<p><span style="background: linear-gradient(to right, #FFA7A3, #5673BD); padding: 0.43em 1em; font-size: 25px; border-radius: 3px; color: #FFFFFF;">1 Team Iot Project!</span></p>
<a href="1p"><button style="WIDTH: 60pt; HEIGHT: 60pt">1 point</button></a>
<a href="2p"><button style="WIDTH: 60pt; HEIGHT: 60pt">2 point</button></a>
<a href="3p"><button style="WIDTH: 60pt; HEIGHT: 60pt">3 point</button></a>
<a href="4p"><button style="WIDTH: 60pt; HEIGHT: 60pt">4 point</button></a>
<a href="cola"><button style="background-color: red; WIDTH: 60pt; HEIGHT: 60pt;">Cola</button></a>
<a href="cider"><button style="background-color: green; WIDTH: 60pt; HEIGHT: 60pt;">Cider</button></a>
<a href="fanta"><button style="background-color: orange; WIDTH: 60pt; HEIGHT: 60pt;">Fanta</button></a>
<div style="text-align : center; ">
  <img src="https://uyjoqvxyzgvv9714092.cdn.ntruss.com/data2/content/image/2021/10/05/20211005319942.jpg"/>
</div>
</center>
</body>
</html>
)rawliteral";
int a=30;
int a_open=80;
int b=90;
int c=70;
int d=30;
AsyncWebServer server(80);
// 페이지 요청이 들어오면 처리하는 함수
String processor(const String& var)
{
  Serial.println(var);
  return var;
}
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.println("ESP32 Web Server Start");
  Serial.println(ssid);
  // WiFi 접속
  WiFi.begin(ssid, password);
  // 접속 체크
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
    Serial.print(".");
  }
  Serial.println();
  // 접속 완료
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  // 서보모터 핀 번호 설정
  servo1.attach(22);
  servo2.attach(21);
  servo4.attach(19);
  servo5.attach(18);
  // callback 함수 등록
  server.on("/", HTTP_GET, [] (AsyncWebServerRequest *req){
    req->send_P(200, "text.html", html, processor);
  });
  server.on("/1p", HTTP_GET, [] (AsyncWebServerRequest *req){
    Serial.println("target1");
    req->send_P(200, "text.html", html, processor);
  });
  server.on("/2p", HTTP_GET, [] (AsyncWebServerRequest *req){
    Serial.println("target2");
    req->send_P(200, "text.html", html, processor);
  });
  server.on("/3p", HTTP_GET, [] (AsyncWebServerRequest *req){
    Serial.println("target3");
    req->send_P(200, "text.html", html, processor);
  });
  server.on("/4p", HTTP_GET, [] (AsyncWebServerRequest *req){
    Serial.println("target4");
    req->send_P(200, "text.html", html, processor);
  });
  server.on("/cola", HTTP_GET, [] (AsyncWebServerRequest *req){
    Serial.println("cola");
    req->send_P(200, "text.html", html, processor);
  });
  server.on("/cider", HTTP_GET, [] (AsyncWebServerRequest *req){
    Serial.println("cider");
    req->send_P(200, "text.html", html, processor);
  });
  server.on("/fanta", HTTP_GET, [] (AsyncWebServerRequest *req){
    Serial.println("fanta");
    req->send_P(200, "text.html", html, processor);
  });
  server.begin();
  Serial.println("HTTP Server Started!");
  delay(100);
}

void loop() 
{
  if(Serial.available())
  {
    input = (char)Serial.read();
    if (input == 'p' || input == 'c')
    {
      Serial.println(input);
      a=30;
      b=90;
      c=70;
      d=0;
      e=c;
      servo1.write(a_open);
      delay(2000);

      for(int i = 30 ; i> d;i = i-2)
      {
        servo5.write(i);
        delay(del);
      }
      for(int i = 75 ; i> c;i = i-2)
      {
        servo4.write(i);
        delay(del);
      } 

      char input = 'k';
    }
    if (input == 'j')
    {
      Serial.println(input);
      a=20;
      b=90;
      c=50;
      d=0;
      e=c;
      servo1.write(a_open);
      delay(2000);

      for(int i = 30 ; i> d;i = i-2)
      {
        servo5.write(i);
        delay(del);
      }
      for(int i = 75 ; i> c;i = i-2)
      {
        servo4.write(i);
        delay(del);
      } 

      char input = 'k';
    }
    if (input == 'd')
    {
      Serial.println(input);
      d = 30;
      c = 75;

      for(int i = 0 ; i< d;i = i+2)
      {
        servo5.write(i);
        delay(del);
      }
      for(int i = e ; i< c;i = i+2)
      {
        servo4.write(i);
        delay(del);
      } 

      char input = 'k';
    }
    if (input == 'q')
    {
      Serial.println(input);
      servo1.write(a_open);
      a = 30;
      char input = 'k';
    }
  }
  
  servo2.write(b);  
  servo4.write(c); 
  servo5.write(d);     //5번모터 각도 설정
  delay(2000);
  servo1.write(a);
}