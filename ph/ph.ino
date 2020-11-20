
#include <Wire.h>
#define I2C_SLAVE_ADDRESS 11

String sensor;

 
void setup() {
  Serial.begin(9600);
  Wire.begin(I2C_SLAVE_ADDRESS);                // join i2c bus with address #11
  Wire.onRequest(requestEvent); // register event
  Wire.onReceive(receiveEvents);

}

void loop() {
  delay(100);
}


void requestEvent() { // if request send from raspi, we will respond with "ek"
  String response;
  char buffer[16];
  if(sensor =="ph"){
    response = "sample data";
    }
  else if(sensor == "turbidity"){
    response = "TBsen";
      }
   else{
    response = "hello";
    }
  response.toCharArray(buffer, 16);
  Wire.write(buffer); 
  Serial.println("responsed");
}
void receiveEvents(int numBytes) // if some data has been recieved from raspi
{  
  String request;
  while(Wire.available()){
    int number = Wire.read();
    request = (char)number;
    Serial.println(request);
  }
  if(request == "1"){
    sensor = "ph";
  }
  if(request == "2"){
    sensor = "turbidity";
    }  
}
