# BRL Syntax & Semantic Analysis - C++ Rules Implementation

## Overview
This document details all C++ syntax and semantic rules enforced by the BRL compiler's Parser and Semantic Analyzer phases.

---

# PART 1: SYNTAX ANALYSIS (Parser)

The Parser validates the **grammatical structure** of statements following C++ syntax rules.

---

## 1. STATEMENT STRUCTURE RULE (C++ Standard)

### ✅ REQUIRED Structure:
```
[DATATYPE] [IDENTIFIER] [ASSIGN] [LITERAL] [DELIMITER]
```

**Exactly 5 tokens** in this exact order.

### Example:
```brl
sigma age rizz 100!
│     │   │    │   │
│     │   │    │   └── DELIMITER (!)
│     │   │    └────── LITERAL (100)
│     │   └─────────── ASSIGN (rizz)
│     └─────────────── IDENTIFIER (age)
└───────────────────── DATATYPE (sigma)
```

**Parser validation:**
- ✅ Position 0: DATATYPE
- ✅ Position 1: IDENTIFIER
- ✅ Position 2: ASSIGN (rizz)
- ✅ Position 3: LITERAL
- ✅ Position 4: DELIMITER (!)

---

## 2. TOKEN COUNT VALIDATION (C++ Strict Rule)

### ✅ VALID: Exactly 5 Tokens
```brl
sigma age rizz 100!        ✓ Valid (5 tokens)
```

### ❌ INVALID: Too Few Tokens (< 5)
```brl
sigma age rizz 100         ✗ Missing delimiter (4 tokens)
sigma age 100!             ✗ Missing assign operator (4 tokens)
sigma rizz 100!            ✗ Missing identifier (4 tokens)
age rizz 100!              ✗ Missing datatype (4 tokens)
```

**Error message:**
```
❌ [PARSER] ERROR: Expected 5 tokens, but found 4.
[PARSER] Missing components in statement structure.
```

---

### ❌ INVALID: Too Many Tokens (> 5)

In C++, multiple statements on one line require proper delimiters:
```cpp
// C++ Example
int x=100, y=200;  // Allowed with comma separator
int x=100 200;     // ERROR! Extra token
```

BRL follows C++ strictly:
```brl
sigma age rizz 100 200!    ✗ Extra token "200" (6 tokens)
sigma x rizz 100! sigma y rizz 200!  ✗ Two statements without proper separation
```

**Error message:**
```
❌ [PARSER] ERROR: Expected 5 tokens, but found 6.
[PARSER] Extra tokens detected after delimiter: ['200']
[PARSER] C++ Rule: Only one statement per line allowed.
```

---

## 3. POSITION 0: DATATYPE VALIDATION

### ✅ VALID Datatypes:
```brl
sigma    ✓ Integer type
gyatt    ✓ String type
smol     ✓ Float type
```

### ❌ INVALID:
```brl
age rizz 100!              ✗ Missing datatype (starts with identifier)
123 rizz 100!              ✗ Starts with numeric literal
rizz age rizz 100!         ✗ Starts with keyword (not a datatype)
```

**C++ Equivalent:**
```cpp
int x = 100;     // ✓ Valid - explicit type
x = 100;         // ✓ Valid in C++ (if x declared earlier)
                 // ✗ Invalid in BRL (requires explicit type)
```

**BRL requires explicit type declaration** for all variable declarations (like C++11 without auto).

---

## 4. POSITION 1: IDENTIFIER VALIDATION

### ✅ VALID Identifiers:
```brl
sigma age rizz 100!        ✓ Valid identifier
sigma _count rizz 100!     ✓ Starts with underscore
sigma player1 rizz 100!    ✓ Digit at end
```

### ❌ INVALID Identifiers:

**Case 1: Keyword as Identifier**
```brl
sigma sigma rizz 100!      ✗ "sigma" is a keyword (datatype)
sigma rizz rizz 100!       ✗ "rizz" is a keyword (assign)
```

**Error message:**
```
❌ [PARSER] Position 1 ERROR: 'sigma' is not a valid IDENTIFIER
   HINT: 'sigma' is a keyword (datatype), cannot be used as variable name
```

**Case 2: Literal as Identifier**
```brl
sigma 123 rizz 100!        ✗ Numeric literal instead of identifier
sigma "name" rizz 100!     ✗ String literal instead of identifier
```

**Error message:**
```
❌ [PARSER] Position 1 ERROR: '123' is not a valid IDENTIFIER
   HINT: '123' is a literal, not an identifier
```

**C++ Equivalent:**
```cpp
int int = 100;       // ✗ ERROR: 'int' is a keyword
int 123 = 100;       // ✗ ERROR: Invalid identifier
```

---

## 5. POSITION 2: ASSIGNMENT OPERATOR VALIDATION

### ✅ VALID:
```brl
sigma age rizz 100!        ✓ "rizz" is the assignment operator
```

### ❌ INVALID:
```brl
sigma age = 100!           ✗ "=" not recognized (use "rizz")
sigma age sigma 100!       ✗ Wrong keyword
sigma age 100!             ✗ Missing assignment operator
```

**Error message:**
```
❌ [PARSER] Position 2 ERROR: '=' is not the assignment operator
   HINT: Use 'rizz' for assignment (equivalent to '=' in C++)
```

---

## 6. POSITION 3: LITERAL VALIDATION

### ✅ VALID Literals:
```brl
sigma age rizz 100!        ✓ Integer literal
smol temp rizz 98.6!       ✓ Float literal
gyatt name rizz "John"!    ✓ String literal
```

### ❌ INVALID:
```brl
sigma age rizz x!          ✗ Identifier instead of literal
sigma age rizz sigma!      ✗ Keyword instead of literal
```

**Error message:**
```
❌ [PARSER] Position 3 ERROR: 'x' is not a valid LITERAL
   HINT: Expected a number, string, or constant (bet/cooked/ligma)
```

---

## 7. POSITION 4: DELIMITER VALIDATION

### ✅ VALID:
```brl
sigma age rizz 100!        ✓ Statement ends with "!"
```

### ❌ INVALID:
```brl
sigma age rizz 100         ✗ Missing delimiter
sigma age rizz 100;        ✗ Wrong delimiter (";" not recognized)
```

**Error message:**
```
❌ [PARSER] Position 4 ERROR: Missing statement delimiter
   HINT: Every statement must end with '!' (equivalent to ';' in C++)
```

**C++ Equivalent:**
```cpp
int x = 100;     // ✓ Valid - ends with semicolon
int x = 100      // ✗ ERROR: Missing semicolon
```

---

# PART 2: SEMANTIC ANALYSIS

The Semantic Analyzer validates **meaning and correctness** of code following C++ semantic rules.

---

## 1. VARIABLE REDECLARATION DETECTION (C++ Rule)

### C++ Rule:
> In C++, you cannot redeclare a variable in the same scope.

### ✅ ALLOWED: Different Variables
```brl
sigma x rizz 100!          ✓ Declare x
sigma y rizz 200!          ✓ Declare y (different variable)
sigma z rizz 300!          ✓ Declare z (different variable)
```

### ❌ FORBIDDEN: Redeclaration in Same Scope
```brl
sigma x rizz 100!          ✓ First declaration
sigma x rizz 200!          ✗ ERROR: Redeclaration in same scope
```

**Error message:**
```
❌ [SEMANTICS] FATAL ERROR: Variable redeclaration detected!
   Variable 'x' already declared in this scope (Level 0).
[SEMANTICS] C++ Rule: Cannot redeclare variable in the same scope.
[SEMANTICS] Recovery Strategy: Compiler will discard this declaration.
```

**C++ Equivalent:**
```cpp
int x = 100;
int x = 200;   // ✗ ERROR: redeclaration of 'x'
```

---

## 2. VARIABLE SHADOWING (C++ Allowed)

### C++ Rule:
> Variables in nested scopes CAN shadow outer scope variables.

### ✅ ALLOWED: Shadowing in Nested Scope
```brl
sigma x rizz 100!          ✓ Declare x in global scope (Level 0)
{
  sigma x rizz 200!        ✓ Declare x in nested scope (Level 1)
}                          ✓ ALLOWED: Different scopes
```

**Semantic messages:**
```
✓ [SEMANTICS] Variable 'x' is not previously declared.     (at Level 0)
⚠️ [SEMANTICS] WARNING: Variable 'x' shadows variable from outer scope (Level 0).
[SEMANTICS] C++ Rule: Shadowing is allowed but may cause confusion.
```

**Symbol Table:**
```
Variable   Data Type   Level   Offset
x          sigma       0       0        ← Outer scope
x          sigma       1       1        ← Inner scope (shadows outer)
```

**C++ Equivalent:**
```cpp
int x = 100;      // Outer scope
{
    int x = 200;  // ✓ Inner scope (shadows outer x)
}
```

---

## 3. STRICT TYPE CHECKING (C++ No Implicit Conversion)

### C++ Rule:
> BRL follows C++'s strict type system - no implicit conversions between incompatible types.

---

### Test Case 1: INTEGER Type (sigma)

#### ✅ VALID:
```brl
sigma age rizz 100!        ✓ Integer literal (no decimal point)
sigma count rizz 0!        ✓ Zero
sigma total rizz 9999!     ✓ Large integer
```

#### ❌ INVALID:
```brl
sigma age rizz 100.0!      ✗ Float literal (has decimal point)
sigma age rizz "100"!      ✗ String literal
sigma age rizz 3.14!       ✗ Float literal
```

**Error message:**
```
❌ [SEMANTICS] FATAL ERROR: Type mismatch detected!
   Expected: INTEGER, but got: FLOAT
   Variable 'age' is declared as 'sigma', but value '100.0' is FLOAT.
[SEMANTICS] C++ Rule: No implicit type conversion allowed between incompatible types.
```

**C++ Equivalent:**
```cpp
int x = 100;      // ✓ Valid
int x = 100.0;    // ⚠️ Warning: implicit conversion from double to int
                  // BRL is stricter - rejects this
```

---

### Test Case 2: FLOAT Type (smol)

#### ✅ VALID:
```brl
smol temp rizz 98.6!       ✓ Float literal (has decimal point)
smol ratio rizz 0.5!       ✓ Decimal less than 1
smol pi rizz 3.14159!      ✓ Float value
```

#### ❌ INVALID:
```brl
smol temp rizz 100!        ✗ Integer literal (no decimal point)
smol temp rizz "98.6"!     ✗ String literal
```

**Error message:**
```
❌ [SEMANTICS] FATAL ERROR: Type mismatch detected!
   Expected: FLOAT, but got: INTEGER
   Variable 'temp' is declared as 'smol', but value '100' is INTEGER.
[SEMANTICS] C++ Rule: No implicit type conversion allowed between incompatible types.
```

**C++ Equivalent:**
```cpp
float x = 98.6;    // ✓ Valid
float x = 100;     // ⚠️ Warning: implicit conversion from int to float
                   // BRL is stricter - rejects this
```

---

### Test Case 3: STRING Type (gyatt)

#### ✅ VALID:
```brl
gyatt name rizz "John"!         ✓ String literal (in quotes)
gyatt msg rizz "Hello World"!   ✓ String with spaces
gyatt empty rizz ""!            ✓ Empty string
```

#### ❌ INVALID:
```brl
gyatt name rizz 123!            ✗ Integer literal
gyatt name rizz 3.14!           ✗ Float literal
gyatt name rizz John!           ✗ Identifier (not quoted)
```

**Error message:**
```
❌ [SEMANTICS] FATAL ERROR: Type mismatch detected!
   Expected: STRING, but got: INTEGER
   Variable 'name' is declared as 'gyatt', but value '123' is INTEGER.
[SEMANTICS] C++ Rule: No implicit type conversion allowed between incompatible types.
```

**C++ Equivalent:**
```cpp
std::string name = "John";  // ✓ Valid
std::string name = 123;     // ✗ ERROR: Cannot convert int to string
```

---

## 4. INTEGER vs FLOAT DISTINCTION (C++ Strict)

### C++ Rule:
> BRL strictly distinguishes between INTEGER and FLOAT based on literal format.

### Distinction Rules:
- `100` → **INTEGER** (no decimal point)
- `100.0` → **FLOAT** (has decimal point)
- `0` → **INTEGER**
- `0.0` → **FLOAT**

### Examples:

```brl
sigma x rizz 100!      ✓ Valid: INTEGER literal to INTEGER type
sigma x rizz 100.0!    ✗ Error: FLOAT literal to INTEGER type

smol y rizz 100.0!     ✓ Valid: FLOAT literal to FLOAT type
smol y rizz 100!       ✗ Error: INTEGER literal to FLOAT type
```

**Test Matrix:**

| Declaration | Value  | Expected | Actual  | Result |
|-------------|--------|----------|---------|--------|
| `sigma`     | `100`  | INTEGER  | INTEGER | ✓ PASS |
| `sigma`     | `100.0`| INTEGER  | FLOAT   | ✗ FAIL |
| `smol`      | `100.0`| FLOAT    | FLOAT   | ✓ PASS |
| `smol`      | `100`  | FLOAT    | INTEGER | ✗ FAIL |
| `gyatt`     | `"100"`| STRING   | STRING  | ✓ PASS |
| `gyatt`     | `100`  | STRING   | INTEGER | ✗ FAIL |

---

## 5. TYPE CHECKING ALGORITHM

```python
def _get_actual_type(literal_token):
    """
    Determine actual type from literal token.
    C++ Rule: Strict distinction between int and float
    """
    if literal_token.type == STRING_LITERAL:
        return "STRING"

    elif literal_token.type == NUMERIC_LITERAL:
        # C++ Rule: Check for decimal point
        if '.' in literal_token.value:
            return "FLOAT"      # Has decimal → float
        else:
            return "INTEGER"    # No decimal → int

    elif literal_token.type in [TRUE_BET, FALSE_COOKED]:
        return "BOOLEAN"

    elif literal_token.type == NULL_LIGMA:
        return "NULL"

    return "UNKNOWN"
```

---

## 6. SYMBOL TABLE BINDING (C++ Memory Model)

### Binding Process:
1. **Check redeclaration** in same scope → ERROR if found
2. **Check type compatibility** → ERROR if mismatch
3. **Bind to symbol table** with:
   - Variable name
   - Data type (sigma/gyatt/smol)
   - Scope level (0=global, 1+=nested)
   - Memory offset (auto-incrementing)

### Example:
```brl
sigma points rizz 100!
smol health rizz 95.5!
{
  gyatt rank rizz "S-Tier"!
  sigma ammo rizz 30!
}
```

**Symbol Table:**
```
Variable   Data Type   Level   Offset
points     sigma       0       0
health     smol        0       1
rank       gyatt       1       2
ammo       sigma       1       3
```

**Binding logs:**
```
[SEMANTICS] Binding variable 'points' to Symbol Table...
[SEMANTICS] Scope Level: 0, Memory Offset: 0
✓ [SEMANTICS] Variable 'points' successfully bound to symbol table.
```

---

## 7. ERROR RECOVERY STRATEGY

### C++ Approach:
> When semantic error detected, discard the assignment to prevent corruption.

**Example:**
```brl
sigma age rizz "Twenty"!       ✗ Type mismatch
```

**Recovery:**
```
❌ [SEMANTICS] FATAL ERROR: Type mismatch detected!
[SEMANTICS] Recovery Strategy: Compiler will discard assignment to prevent memory corruption.
```

**Result:**
- Variable `age` is **NOT** added to symbol table
- Compilation marked as failed
- Next statement continues to process (if any)

---

## SUMMARY: C++ COMPLIANCE MATRIX

| Feature | C++ Behavior | BRL Implementation | Status |
|---------|--------------|-------------------|--------|
| Explicit type declaration | Required | Required | ✅ |
| Statement delimiter | Semicolon (;) | Exclamation (!) | ✅ |
| Token count strictness | Exact | Exact (5 tokens) | ✅ |
| Extra tokens after delimiter | Error | Error | ✅ |
| Keywords as identifiers | Forbidden | Forbidden | ✅ |
| Variable redeclaration (same scope) | Error | Error | ✅ |
| Variable shadowing (diff scope) | Warning/Allowed | Warning/Allowed | ✅ |
| Implicit int→float conversion | Warning | Error (stricter) | ✅ |
| Implicit float→int conversion | Warning | Error (stricter) | ✅ |
| String type safety | Strict | Strict | ✅ |
| INT vs FLOAT distinction | By literal format | By decimal point | ✅ |

---

## CONCLUSION

BRL Compiler's **Syntax and Semantic Analysis phases fully comply with C++ standards**, with even **stricter type checking** than standard C++ (no implicit numeric conversions).

**Key Achievements:**
- ✅ Exact token count validation (no extra tokens)
- ✅ Position-based syntax validation
- ✅ Variable redeclaration detection
- ✅ Variable shadowing support (nested scopes)
- ✅ Strict type checking (no implicit conversions)
- ✅ C++-style error messages and recovery
- ✅ Symbol table with scope levels and offsets

**BRL = C++ Compliant Compiler! 🎓**
