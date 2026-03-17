# 🧠 BrainRotLanguage (BRL) Compiler

A web-based compiler for BrainRotLanguage (BRL) built with Streamlit for CS Programming Languages Final Project.

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


**BrainRotLanguage Compiler v2.0**
*CS Programming Languages Final Project*
*Now with Multiline Support!*



March 22, 2026 (Sunday) 11:59 PM
