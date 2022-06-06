#include <TimerOne.h> // подключаем библиотеку TimerOne для задействования функций Таймера1 
float val = 0; 

void sendData() {    
  val = analogRead(A1);        
  Serial.write(int(val/1023*200));   
  val = analogRead(A0);        
  Serial.write(int(val/1023*200)); 
  Serial.write(255);  
}

void setup() {
  Serial.begin(9600);                    
  Timer1.initialize(3000);                                                         
  Timer1.attachInterrupt(sendData);     
}

void loop() {
}