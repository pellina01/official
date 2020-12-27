
#define SensorPinph 0   //pH meter Analog output to Arduino Analog Input 0
#define SensorPinturb 1 //turb meter Analog output to Arduino Analog Input 0
#include <Wire.h>
#define I2C_SLAVE_ADDRESS 11

String sensor;

void setup()
{

  Wire.begin(I2C_SLAVE_ADDRESS); // join i2c bus with address #11
  Wire.onRequest(requestEvent);  // register event
  Wire.onReceive(receiveEvents);

  Serial.begin(9600);
  Serial.println("Ready"); //Test the serial monitor
}
void loop()
{
}

void requestEvent()
{ // if request send from raspi, we will respond with "ek"
  float response;
  char buffer[16];
  if (sensor == "ph")
  {
    response = ph();
  }
  else if (sensor == "turbidity")
  {
    response = turb();
  }
  dtostrf(response, 13, 2, buffer);
  Wire.write(buffer);
  Serial.println("responsed");
}

void receiveEvents(int numBytes) // if some data has been recieved from raspi
{
  String request;
  while (Wire.available())
  {
    int number = Wire.read();
    request = (char)number;
    Serial.println(request);
  }
  if (request == "1")
  {
    sensor = "ph";
  }
  if (request == "2")
  {
    sensor = "turbidity";
  }
}

float ph()
{
  unsigned long int avgValue; //Store the average value of the sensor feedback
  float b;
  int buf[10], temp;

  for (int i = 0; i < 10; i++) //Get 10 sample value from the sensor for smooth the value
  {
    buf[i] = analogRead(SensorPinph);
    delay(100);
  }
  for (int i = 0; i < 9; i++) //sort the analog from small to large
  {
    for (int j = i + 1; j < 10; j++)
    {
      if (buf[i] > buf[j])
      {
        temp = buf[i];
        buf[i] = buf[j];
        buf[j] = temp;
      }
    }
  }
  avgValue = 0;
  for (int i = 2; i < 8; i++)
  { //take the average value of 6 center sample
    avgValue += buf[i];
  }

  float phValue = (float)avgValue * 5.0 / 1024 / 6; //convert the analog into millivolt
  phValue = (13.63 * phValue - 19.68);              //convert the millivolt into pH value
  return (phValue);
}

float turb()
{
  float ntu;
  float volt1;
  int sensorValue = analogRead(SensorPinturb); // read the input on analog pin 0:
  volt1 = sensorValue * (5.0 / 1024.0);        // Convert the analog reading (which goes from 0 - 1023) to a voltage (0 - 5V):
  if (volt1 < 2.5)
  {
    ntu = 3000;
  }
  else if (volt1 > 4.19)
  {
    ntu = 10;
  }
  else
  {
    ntu = -1120.4 * square(volt1) + 5742.3 * volt1 - 4353.8;
  }
  return ntu;
}
