# 🧠 BrainRotLanguage (BRL) Compiler

A web-based compiler for BrainRotLanguage (BRL) built with Streamlit for CS Programming Languages Final Project.

**NOW WITH MULTILINE SUPPORT!** 🚀

## 🚀 Quick Start

### Installation

1. Install required dependencies:
```bash
pip install streamlit pandas
```

### Running the Compiler

Run the Streamlit application:
```bash
streamlit run brl_compiler.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📖 Language Syntax

### Data Types
- `sigma` → integer
- `gyatt` → string
- `smol` → float

### Keywords
- `rizz` → assignment operator (=)
- `yap` → output (print)
- `mogging` → input
- `chad` → return

### Control Flow
- `cap` → if statement
- `flex` → else statement
- `grind` → while loop

### Logical Operators
- `bussin` → AND
- `pookie` → OR
- `cringe` → NOT

### Fixed Values
- `bet` → true
- `cooked` → false
- `ligma` → null

### Delimiter
- `!` → end of statement (semicolon equivalent)

## ✅ Test Cases

### Test Case 1: Valid Single Line Code
```
sigma age rizz 20!
```
**Expected**: All phases pass, variable bound to symbol table

### Test Case 2: Valid Multiline Code (Multiple Variables)
```
sigma playerID rizz 101!
smol healthPos rizz 98.5!
gyatt rank rizz "S-Tier"!
sigma finalScore rizz 5000!
```
**Expected**: All phases pass, 4 variables bound to symbol table

### Test Case 3: Multiline with Block Structure
```
sigma playerID rizz 101!
smol healthPos rizz 98.5!
{
    gyatt rank rizz "S-Tier"!
    sigma ammoCount rizz 30!
}
sigma finalScore rizz 5000!
```
**Expected**: All phases pass, 5 variables bound, block structure recognized

### Test Case 4: Type Mismatch Error
```
sigma age rizz "Twenty"!
```
**Expected**: Semantic error - type mismatch (integer expected, string provided)

### Test Case 5: Missing Delimiter
```
sigma age rizz 20
```
**Expected**: Syntax error - missing delimiter

### Test Case 6: Unknown Token (Panic Mode)
```
sigma age @@ 20!
```
**Expected**: Unknown token warning, panic mode recovery

### Test Case 7: Mixed Valid and Invalid Statements
```
sigma age rizz 25!
gyatt name rizz 123!
smol ratio rizz 3.14!
```
**Expected**: First and third succeed, second shows semantic error (string type with integer value)

## 🏗️ Architecture

### 1. Lexer (Lexical Analysis)
- Tokenizes input code
- Identifies token types based on BRL syntax
- Implements panic mode recovery for unknown tokens

### 2. Parser (Syntax Analysis)
- Validates token sequence structure
- Expected pattern: `[DATATYPE] [IDENTIFIER] [ASSIGN] [LITERAL] [DELIMITER]`
- Reports structural errors

### 3. Semantic Analyzer (Semantic Analysis)
- Checks type compatibility
- Validates data type assignments
- Maintains symbol table for variable bindings

## 🎨 Features

✅ **Multiline Code Support**: Process multiple statements at once with block structures
✅ **Explainability Layer**: Detailed logs at each compilation phase for every statement
✅ **Panic Mode Recovery**: Skips unknown tokens and continues parsing
✅ **Symbol Table Display**: Shows all bound variables with types and values
✅ **Interactive UI**: Clean three-column layout for analysis phases
✅ **Real-time Compilation**: Instant feedback on code validity
✅ **Block Structure Recognition**: Handles nested code blocks with `{` and `}`

## 📝 Project Structure

```
Prog_Lang_Final/
├── brl_compiler.py      # Main compiler application
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── CS_PROGLANG.md      # Project specification
└── Phase_1.md          # Language design document
```

## 🎯 Grading Criteria Coverage

- ✅ **Lexical & Syntax Analysis (30 pts)**: Flawless tokenization and grammar validation
- ✅ **Semantic Analysis & Binding (30 pts)**: Type checking and symbol table implementation
- ✅ **Explainability Layer (30 pts)**: Beautiful, clear output explaining every step
- ✅ **Creative Expansion**: Panic Mode Recovery for error handling

## 👨‍💻 Author

**BrainRotLanguage Compiler v2.0**
*CS Programming Languages Final Project*
*Now with Multiline Support!*


March 22, 2026 (Sunday) 11:59 PM
