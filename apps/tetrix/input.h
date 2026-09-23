class Input {
public:
  // Puts the terminal in raw mode (no line buffering/echo) once for the
  // session. pollKey() only works as a non-blocking read after this.
  static void enableRawMode();
  static void restoreMode();
  static bool pollKey(char& c);
};
