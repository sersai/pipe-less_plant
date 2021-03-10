char letter;
int k  = 0;
char message[256];
unsignied int tt;
int init_delay = 1000;
int loop_delay = 250;
int baudrate = 115200;
void setup(){
  Serial.begin(baudrate);
  Serial3.begin(baudrate);
  delay(init_delay);
  Serial.println("Configuration Complete");
  Serial3.write("AT+Scan=OFF\r");
}
void loop (){
  Serial3.write("AT+Inventory\r");
  tt = millis();
  Serial.print(tt);
  Serial.print('\n');
  k = 0;
  for(int i = 0; i <= 255; i++){
    message[i]='';
  }
  delay(loop_delay);
  while(Serial3.available() > 0){
    if(Serial3.available() > 0){
      letter = Serial3.read();
      k = k+1;
    }
  }
  message[k]='\0';
  Serial.println(message);
}