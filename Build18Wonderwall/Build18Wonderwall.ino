/**
 * @file Build18Wonderwall.ino
 * 
 * Guitar That Only Plays Wonderwall
 *
 * @brief Arduino sketch for Guitar That Only Plays Wonderwall. 
 *        Plays guitar chords by activating transistors connected to 
 *        solenoids above the frets and turns servos to pluck the strings.
 *        Targets the Raspberry Pi Pico. 
 *
 **/

//////////////////////////////////////////////////////////////////////////
// Libraries, Macro, and Variable Definitions
//////////////////////////////////////////////////////////////////////////

#include <Servo.h>

// Toggled Servo Angles
#define SERVO_POS_0 0  // Default position
#define SERVO_POS_1 20

#define OPEN 31

// Strings
#define e_STRING_PIN 0 // 1
#define B_STRING_PIN 1 // 2
#define G_STRING_PIN 2 // 3
#define D_STRING_PIN 3 // 4
#define A_STRING_PIN 4 // 5
#define E_STRING_PIN 5 // 6

// First Fret
#define e_1  // NC
#define B_1 6
#define G_1  // NC
#define D_1  // NC
#define A_1  // NC
#define E_1  // NC

// Second Fret
#define e_2 7
#define B_2 8
#define G_2 9
#define D_2 10
#define A_2 11
#define E_2  // NC

// Third Fret
#define e_3 12
#define B_3 13
#define G_3  // NC
#define D_3  // NC
#define A_3 14
#define E_3 15

#define BAUDRATE 115200

typedef struct chord_t {
  String name;
  int e_string_note;
  int B_string_note;
  int G_string_note;
  int D_string_note;
  int A_string_note;
  int E_string_note;
  char mask;  // Binary mask for which strings to play
              // Bit position:  876543210
              // Guitar String: --EADGBe-
} chord_t;

// Chords
chord_t Em;
chord_t G;
chord_t D;
chord_t A;
chord_t C;

// Create Servo objects
Servo servo_e;
Servo servo_B;
Servo servo_G;
Servo servo_D;
Servo servo_A;
Servo servo_E;

// Variables
int servo_e_pos;
int servo_B_pos;
int servo_G_pos;
int servo_D_pos;
int servo_A_pos;
int servo_E_pos;

long pins_state; // Bitmask where each bit position corresponds to the pin number
                // i.e. ..001100 would mean pins 2 and 3 are on, the rest are off
// long valid_pins = 0b110111101111011110110;
long valid_pins = 0b1111111111111111;


//////////////////////////////////////////////////////////////////////////
// Functions
//////////////////////////////////////////////////////////////////////////

void setup() {
  // put your setup code here, to run once:

  // Attach servos
  servo_e.attach(e_STRING_PIN);
  servo_B.attach(B_STRING_PIN);
  servo_G.attach(G_STRING_PIN);
  servo_D.attach(D_STRING_PIN);
  servo_A.attach(A_STRING_PIN);
  servo_E.attach(E_STRING_PIN);

  // Initialize pins
  pinMode(B_1, OUTPUT);

  pinMode(e_2, OUTPUT);
  pinMode(B_2, OUTPUT);
  pinMode(G_2, OUTPUT);
  pinMode(D_2, OUTPUT);
  pinMode(A_2, OUTPUT);

  pinMode(e_3, OUTPUT);
  pinMode(B_3, OUTPUT);
  pinMode(A_3, OUTPUT);
  pinMode(E_3, OUTPUT);

  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);

  // Set up chord data structures
  //                Name,  e,    B,    G,    D,    A,    E,     mask
  Em = format_chord("Em", OPEN, OPEN, OPEN, D_2, A_2, OPEN, 0b1111110);
  G = format_chord("G", e_3, OPEN, OPEN, OPEN, A_2, E_3, 0b1111110);
  D = format_chord("D", e_2, B_3, G_2, OPEN, OPEN, OPEN, 0b0011110);
  A = format_chord("A", OPEN, B_2, G_2, D_2, OPEN, OPEN, 0b0111110);
  C = format_chord("C", OPEN, B_1, OPEN, D_2, A_3, OPEN, 0b0111110);

  // Begin Serial Communication
  Serial.begin(BAUDRATE);
  Serial.print("Connecting to serial port...");
  Serial.print("\n");

  // Test each chord
  play_chord(Em);
  delay(1000);
  play_chord(G);
  delay(1000);
  play_chord(D);
  delay(1000);
  play_chord(A);
  delay(1000);
  play_chord(C);
  delay(1000);
}

void loop() {
  // put your main code here, to run repeatedly:

  if (Serial.available()){
    Serial.print("Data received: ");
    String data = Serial.readStringUntil('\n');
    Serial.print(data);
    Serial.print("\n");

    if (data.equals("Em")) { play_chord(Em); }
    else if (data.equals("G")) { play_chord(G); } 
    else if (data.equals("D")) { play_chord(D); }
    else if (data.equals("A")) { play_chord(A); }
    else if (data.equals("C")) { play_chord(C); }

  }

}

chord_t format_chord(String name, int e_note, int B_note, int G_note,
                     int D_note, int A_note, int E_note, int mask) {

  chord_t new_chord;

  new_chord.name = name;
  new_chord.e_string_note = e_note;
  new_chord.B_string_note = B_note;
  new_chord.G_string_note = G_note;
  new_chord.D_string_note = D_note;
  new_chord.A_string_note = A_note;
  new_chord.E_string_note = E_note;
  new_chord.mask = mask;

  return new_chord;
}

void play_chord(chord_t chord) {

  pins_state = 0; // Set all pins OFF

  pins_state |= (1 << chord.e_string_note);
  pins_state |= (1 << chord.B_string_note);
  pins_state |= (1 << chord.G_string_note);
  pins_state |= (1 << chord.D_string_note);
  pins_state |= (1 << chord.A_string_note);
  pins_state |= (1 << chord.E_string_note);

  Serial.println(chord.name);
  Serial.print("Pins: ");
  Serial.print(pins_state, BIN);
  Serial.print("\n");

  press_solenoids(pins_state);
  
  turn_servos(chord.mask);
}

/**
 * @brief Changes Digital pin states based on input
 *
 * @param[in] state bitmask for the state
 */
void press_solenoids(long state) {
  for (int i = 0; i < 32; i++) {
    if (((state & valid_pins) >> i) & 1) { // Pin is valid and ON
      digitalWrite(i, HIGH);
    } else if ((valid_pins >> i) & 1) { // Pin is valid but not ON
      digitalWrite(i, LOW);
    }
  }
}

/**
 * @brief Turns servos based on input mask
 *
 * @param[in] mask bitmask for servos 
 */
void turn_servos(int mask) {
  // Extract infor from mask
  bool play_e = (mask >> 1) & 1;
  bool play_B = (mask >> 2) & 1;
  bool play_G = (mask >> 3) & 1;
  bool play_D = (mask >> 4) & 1;
  bool play_A = (mask >> 5) & 1;
  bool play_E = (mask >> 6) & 1;

  // Set new servo positions
  int new_servo_e_pos = (play_e) ? get_new_servo_pos(servo_e_pos) : servo_e_pos;
  int new_servo_B_pos = (play_B) ? get_new_servo_pos(servo_B_pos) : servo_B_pos;
  int new_servo_G_pos = (play_G) ? get_new_servo_pos(servo_G_pos) : servo_G_pos;
  int new_servo_D_pos = (play_D) ? get_new_servo_pos(servo_D_pos) : servo_D_pos;
  int new_servo_A_pos = (play_A) ? get_new_servo_pos(servo_A_pos) : servo_A_pos;
  int new_servo_E_pos = (play_E) ? get_new_servo_pos(servo_E_pos) : servo_E_pos;

  // Write to new positions to servos
  servo_e.write(new_servo_e_pos);
  servo_B.write(new_servo_B_pos);
  servo_G.write(new_servo_G_pos);
  servo_D.write(new_servo_D_pos);
  servo_A.write(new_servo_A_pos);
  servo_E.write(new_servo_E_pos);

  delay(10);

  servo_e_pos = new_servo_e_pos;
  servo_B_pos = new_servo_B_pos;
  servo_G_pos = new_servo_G_pos;
  servo_D_pos = new_servo_D_pos;
  servo_A_pos = new_servo_A_pos;
  servo_E_pos = new_servo_E_pos;

}

/**
 * @brief Determine new servo position
 *
 * @param[in] servo_pos Old servo_pos
 * @return New servo_pos
 */
int get_new_servo_pos(int servo_pos) {
  if (servo_pos == SERVO_POS_0) {
    return SERVO_POS_1;
  } else {
    return SERVO_POS_0;
  }
}