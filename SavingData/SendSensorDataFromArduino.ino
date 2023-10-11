#define NUM_SENSORS 3 //adjust according to number of simultaenous measurements 
#define SAMPLING_PERIOD 4 //in milliseconds - adjust to meet needs 
int pin_array[5] = {A0,A1,A2,A3,A4}; //use an array to store pin numbers
unsigned long time_ms=0;
int data[NUM_SENSORS];
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  for(int i=0;i<NUM_SENSORS;i++){
      pinMode(pin_array[i],INPUT);
  }
}

void loop() {
  Serial.print(time_ms); //store time from beginning 
  Serial.print(",");
  for(int i=0;i<NUM_SENSORS;i++){  //iterate through measurements from all sensors
    data[i]=analogRead(pin_array[i]);  
    Serial.print(data[i]);
    if(i<NUM_SENSORS-1){
      Serial.print(",");
      }
  }
  Serial.println();
  delay(SAMPLING_PERIOD);
  time_ms+=SAMPLING_PERIOD;
}
