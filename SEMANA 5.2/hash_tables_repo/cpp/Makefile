# =============================================================================
# Makefile — Tabla Hash en C++
# =============================================================================
# Uso:
#   make          → compila el binario
#   make run      → compila y ejecuta
#   make clean    → elimina archivos compilados

CXX      = g++
CXXFLAGS = -std=c++17 -O2 -Wall -Wextra
TARGET   = hash_tables
SRC      = hash_tables.cpp

.PHONY: all run clean

all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SRC)
	@echo "Compilado exitosamente: ./$(TARGET)"

run: $(TARGET)
	./$(TARGET)

clean:
	rm -f $(TARGET)
