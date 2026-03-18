import streamlit as st
import re
import pandas as pd
import html
from enum import Enum
from typing import List, Dict, Tuple, Optional

# ============================================================================
# TOKEN TYPES ENUMERATION
# ============================================================================
class TokenType(Enum):
    # Data Types
    DATATYPE_SIGMA = "DATATYPE_SIGMA"      # int
    DATATYPE_GYATT = "DATATYPE_GYATT"      # string
    DATATYPE_SMOL = "DATATYPE_SMOL"        # float

    # Keywords
    ASSIGN_RIZZ = "ASSIGN_RIZZ"            # assignment operator
    OUTPUT_YAP = "OUTPUT_YAP"              # output keyword
    INPUT_MOGGING = "INPUT_MOGGING"        # input keyword
    RETURN_CHAD = "RETURN_CHAD"            # return keyword

    # Control Flow
    IF_CAP = "IF_CAP"                      # if statement
    ELSE_FLEX = "ELSE_FLEX"                # else statement
    WHILE_GRIND = "WHILE_GRIND"            # while loop

    # Logical Operators
    AND_BUSSIN = "AND_BUSSIN"              # AND operator
    OR_POOKIE = "OR_POOKIE"                # OR operator
    NOT_CRINGE = "NOT_CRINGE"              # NOT operator

    # Fixed Values
    TRUE_BET = "TRUE_BET"                  # true
    FALSE_COOKED = "FALSE_COOKED"          # false
    NULL_LIGMA = "NULL_LIGMA"              # null

    # Literals and Identifiers
    IDENTIFIER = "IDENTIFIER"              # variable names
    NUMERIC_LITERAL = "NUMERIC_LITERAL"    # numbers (int/float)
    STRING_LITERAL = "STRING_LITERAL"      # strings

    # Delimiter
    DELIMITER = "DELIMITER"                # ! (semicolon equivalent)

    # Block Delimiters
    LBRACE = "LBRACE"                      # { (left curly brace)
    RBRACE = "RBRACE"                      # } (right curly brace)

    # Unknown
    UNKNOWN = "UNKNOWN"


# ============================================================================
# TOKEN CLASS
# ============================================================================
class Token:
    def __init__(self, token_type: TokenType, value: str):
        self.type = token_type
        self.value = value

    def __repr__(self):
        return f"Token({self.type.name}, '{self.value}')"


# ============================================================================
# LEXER CLASS - LEXICAL ANALYSIS
# ============================================================================
class Lexer:
    def __init__(self, code: str):
        self.code = code
        self.tokens: List[Token] = []
        self.logs: List[str] = []
        self.unknown_count = 0

        # Keyword mapping
        self.keywords = {
            'sigma': TokenType.DATATYPE_SIGMA,
            'gyatt': TokenType.DATATYPE_GYATT,
            'smol': TokenType.DATATYPE_SMOL,
            'rizz': TokenType.ASSIGN_RIZZ,
            'yap': TokenType.OUTPUT_YAP,
            'mogging': TokenType.INPUT_MOGGING,
            'chad': TokenType.RETURN_CHAD,
            'cap': TokenType.IF_CAP,
            'flex': TokenType.ELSE_FLEX,
            'grind': TokenType.WHILE_GRIND,
            'bussin': TokenType.AND_BUSSIN,
            'pookie': TokenType.OR_POOKIE,
            'cringe': TokenType.NOT_CRINGE,
            'bet': TokenType.TRUE_BET,
            'cooked': TokenType.FALSE_COOKED,
            'ligma': TokenType.NULL_LIGMA,
        }

    def tokenize(self) -> Tuple[List[Token], List[str]]:
        """Perform lexical analysis and return tokens with logs."""
        self.logs.append("--- STARTING LEXICAL ANALYSIS ---")

        # Pattern to properly split tokens including delimiters (C++ rules)
        # Order matters: check for invalid identifiers starting with digits first
        # Matches: strings in quotes, invalid identifiers (digit-start), valid identifiers, numbers, delimiters, unknown
        pattern = r'"[^"]*"|\d+[a-zA-Z_][a-zA-Z0-9_]*|[a-zA-Z_][a-zA-Z0-9_]*|\d+\.?\d*|[!{}]|\S'
        parts = re.findall(pattern, self.code)

        for part in parts:
            # Skip whitespace if any
            if part.strip() == '':
                continue

            token = self._identify_token(part)
            self.tokens.append(token)

            if token.type == TokenType.UNKNOWN:
                self.unknown_count += 1
                self.logs.append(f"[WARNING] [LEXER] Found '{part}' -> UNKNOWN TOKEN (Panic Mode: Skipped)")
            else:
                self.logs.append(f"[SUCCESS] [LEXER] Found '{part}' -> Identified as {token.type.name}")

        # Summary
        if self.unknown_count == 0:
            self.logs.append(f"[SUCCESS] Lexical Analysis Complete. {len(self.tokens)} tokens recognized. 0 Unknown Tokens.")
        else:
            self.logs.append(f"[WARNING] Lexical Analysis Complete. {len(self.tokens)} tokens found. {self.unknown_count} Unknown Tokens skipped.")

        return self.tokens, self.logs

    def _identify_token(self, lexeme: str) -> Token:
        """Identify the token type for a given lexeme."""
        # Check for delimiter
        if lexeme == '!':
            return Token(TokenType.DELIMITER, lexeme)

        # Check for block delimiters
        if lexeme == '{':
            return Token(TokenType.LBRACE, lexeme)
        if lexeme == '}':
            return Token(TokenType.RBRACE, lexeme)

        # Check for string literals (enclosed in quotes)
        # Must have both opening and closing quotes (C++ rule)
        if lexeme.startswith('"'):
            if lexeme.endswith('"') and len(lexeme) >= 2:
                return Token(TokenType.STRING_LITERAL, lexeme)
            else:
                # Unclosed string - invalid in C++
                return Token(TokenType.UNKNOWN, lexeme)

        # Check for keywords (must be checked before identifiers)
        if lexeme in self.keywords:
            return Token(self.keywords[lexeme], lexeme)

        # Check for numeric literals (int or float)
        # Must follow C++ numeric format rules
        if self._is_numeric(lexeme):
            return Token(TokenType.NUMERIC_LITERAL, lexeme)

        # Check for identifiers (variable names)
        # Must follow C++ identifier rules: start with letter or underscore
        if self._is_identifier(lexeme):
            return Token(TokenType.IDENTIFIER, lexeme)

        # Unknown token - anything else is invalid in C++
        return Token(TokenType.UNKNOWN, lexeme)

    def _is_numeric(self, lexeme: str) -> bool:
        """Check if lexeme is a valid number (int or float) following C++ rules."""
        # C++ numeric rules:
        # - Cannot start with multiple zeros (except "0" or "0.x")
        # - Cannot have multiple decimal points
        # - Cannot have letters mixed in (caught by regex, but double-check)

        # Check for invalid patterns like "1.2.3" or "1a2"
        if lexeme.count('.') > 1:
            return False

        # Try parsing as float
        try:
            float(lexeme)
            # Additional check: ensure no letters in the number
            # This catches cases like "123abc" that might slip through
            return True
        except ValueError:
            return False

    def _is_identifier(self, lexeme: str) -> bool:
        """Check if lexeme is a valid identifier following C++ rules."""
        # C++ identifier rules:
        # - Must start with letter (a-z, A-Z) or underscore (_)
        # - Can contain letters, digits, underscores
        # - Cannot start with digit
        # - Cannot contain special characters like -, ., $, @, etc.
        return re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', lexeme) is not None


# ============================================================================
# PARSER CLASS - SYNTAX ANALYSIS
# ============================================================================
class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.logs: List[str] = []
        self.is_valid = False

    def parse(self) -> Tuple[bool, List[str]]:
        """Perform syntax analysis and return validity with logs."""
        self.logs.append("--- STARTING SYNTAX ANALYSIS ---")
        self.logs.append("[PARSER] Checking statement structure...")

        # Filter out UNKNOWN tokens (Panic Mode Recovery)
        valid_tokens = [t for t in self.tokens if t.type != TokenType.UNKNOWN]

        # Expected structure: [DATATYPE] [IDENTIFIER] [ASSIGN] [LITERAL] [DELIMITER]
        self.logs.append("[PARSER] Expected rule: [DATATYPE] [IDENTIFIER] [ASSIGN] [LITERAL] [DELIMITER]")

        # C++ Rule: Exact token count validation
        # Must be exactly 5 tokens (not more, not less)
        if len(valid_tokens) < 5:
            self.logs.append(f"[ERROR] [PARSER] ERROR: Expected 5 tokens, but found {len(valid_tokens)}.")
            self.logs.append("[PARSER] Missing components in statement structure.")
            self.is_valid = False
            return False, self.logs
        elif len(valid_tokens) > 5:
            # C++ doesn't allow extra tokens after delimiter
            self.logs.append(f"[ERROR] [PARSER] ERROR: Expected 5 tokens, but found {len(valid_tokens)}.")
            self.logs.append(f"[PARSER] Extra tokens detected after delimiter: {[t.value for t in valid_tokens[5:]]}")
            self.logs.append("[PARSER] C++ Rule: Only one statement per line allowed.")
            self.is_valid = False
            return False, self.logs

        # Check each position with C++ rules
        errors = []

        # Position 0: DATATYPE (C++ requires type specification)
        if not self._is_datatype(valid_tokens[0]):
            errors.append(f"Position 0: Expected DATATYPE (sigma/gyatt/smol), found {valid_tokens[0].type.name}")
            self.logs.append(f"[PARSER] C++ Rule: Variables must have explicit type declaration.")
        else:
            self.logs.append(f"[SUCCESS] [PARSER] Position 0: '{valid_tokens[0].value}' is a valid DATATYPE")

        # Position 1: IDENTIFIER (C++ requires valid variable name)
        if valid_tokens[1].type != TokenType.IDENTIFIER:
            errors.append(f"Position 1: Expected IDENTIFIER, found {valid_tokens[1].type.name}")
            self.logs.append(f"[PARSER] C++ Rule: Variable name must be a valid identifier.")
        else:
            self.logs.append(f"[SUCCESS] [PARSER] Position 1: '{valid_tokens[1].value}' is a valid IDENTIFIER")

        # Position 2: ASSIGN (C++ requires initialization operator)
        if valid_tokens[2].type != TokenType.ASSIGN_RIZZ:
            errors.append(f"Position 2: Expected ASSIGN (rizz), found {valid_tokens[2].type.name}")
            self.logs.append(f"[PARSER] C++ Rule: Variables must use assignment operator (=).")
        else:
            self.logs.append(f"[SUCCESS] [PARSER] Position 2: '{valid_tokens[2].value}' is a valid ASSIGN operator")

        # Position 3: LITERAL (C++ requires initialization value)
        if not self._is_literal(valid_tokens[3]):
            errors.append(f"Position 3: Expected LITERAL value, found {valid_tokens[3].type.name}")
            self.logs.append(f"[PARSER] C++ Rule: Variables must be initialized with a value.")
        else:
            self.logs.append(f"[SUCCESS] [PARSER] Position 3: '{valid_tokens[3].value}' is a valid LITERAL")

        # Position 4: DELIMITER (C++ requires statement terminator)
        if valid_tokens[4].type != TokenType.DELIMITER:
            errors.append(f"Position 4: Expected DELIMITER (!), found {valid_tokens[4].type.name}")
            self.logs.append(f"[PARSER] C++ Rule: Statements must end with semicolon (!).")
        else:
            self.logs.append(f"[SUCCESS] [PARSER] Position 4: '{valid_tokens[4].value}' is a valid DELIMITER")

        # Report results
        if errors:
            self.logs.append("[ERROR] [PARSER] SYNTAX ERRORS DETECTED:")
            for error in errors:
                self.logs.append(f"   - {error}")
            self.is_valid = False
        else:
            self.logs.append("[SUCCESS] [PARSER] Actual structure matches expected rule perfectly.")
            self.logs.append("[SUCCESS] Syntax Analysis Complete. No structural errors.")
            self.is_valid = True

        return self.is_valid, self.logs

    def _is_datatype(self, token: Token) -> bool:
        """Check if token is a datatype."""
        return token.type in [
            TokenType.DATATYPE_SIGMA,
            TokenType.DATATYPE_GYATT,
            TokenType.DATATYPE_SMOL
        ]

    def _is_literal(self, token: Token) -> bool:
        """Check if token is a literal value."""
        return token.type in [
            TokenType.NUMERIC_LITERAL,
            TokenType.STRING_LITERAL,
            TokenType.TRUE_BET,
            TokenType.FALSE_COOKED,
            TokenType.NULL_LIGMA
        ]


# ============================================================================
# SEMANTIC ANALYZER CLASS - SEMANTIC ANALYSIS
# ============================================================================
class SemanticAnalyzer:
    def __init__(self, tokens: List[Token], current_level: int = 0, current_offset: int = 0):
        self.tokens = tokens
        self.logs: List[str] = []
        self.symbol_table: Dict[str, Dict[str, str]] = {}
        self.is_valid = False
        self.current_level = current_level
        self.current_offset = current_offset

    def analyze(self) -> Tuple[bool, List[str], Dict[str, Dict[str, str]]]:
        """Perform semantic analysis and return validity with logs and symbol table."""
        self.logs.append("--- STARTING SEMANTIC ANALYSIS ---")

        # Filter out UNKNOWN tokens
        valid_tokens = [t for t in self.tokens if t.type != TokenType.UNKNOWN]

        if len(valid_tokens) < 5:
            self.logs.append("[ERROR] [SEMANTICS] ERROR: Insufficient tokens for semantic analysis.")
            return False, self.logs, self.symbol_table

        # Extract components
        datatype_token = valid_tokens[0]
        identifier_token = valid_tokens[1]
        assign_token = valid_tokens[2]
        literal_token = valid_tokens[3]
        delimiter_token = valid_tokens[4]

        # C++ Rule 1: Check for variable redeclaration in the same scope
        self.logs.append("[SEMANTICS] Checking for variable redeclaration...")
        if identifier_token.value in self.symbol_table:
            existing_level = int(self.symbol_table[identifier_token.value]['Level'])
            if existing_level == self.current_level:
                # Redeclaration in the same scope - ERROR in C++
                self.logs.append(f"[ERROR] [SEMANTICS] FATAL ERROR: Variable redeclaration detected!")
                self.logs.append(f"   Variable '{identifier_token.value}' already declared in this scope (Level {self.current_level}).")
                self.logs.append(f"[SEMANTICS] C++ Rule: Cannot redeclare variable in the same scope.")
                self.logs.append("[SEMANTICS] Recovery Strategy: Compiler will discard this declaration.")
                self.is_valid = False
                return False, self.logs, self.symbol_table
            else:
                # Variable exists in different scope - allowed (shadowing)
                self.logs.append(f"[WARNING] [SEMANTICS] WARNING: Variable '{identifier_token.value}' shadows variable from outer scope (Level {existing_level}).")
                self.logs.append(f"[SEMANTICS] C++ Rule: Shadowing is allowed but may cause confusion.")
        else:
            self.logs.append(f"[SUCCESS] [SEMANTICS] Variable '{identifier_token.value}' is not previously declared.")

        # C++ Rule 2: Strict type checking (no implicit conversions)
        self.logs.append("[SEMANTICS] Checking Type Compatibility...")
        self.logs.append(f"[SEMANTICS] Variable '{identifier_token.value}' is declared as '{datatype_token.value}'.")
        self.logs.append(f"[SEMANTICS] Value is '{literal_token.value}' ({literal_token.type.name}).")

        # Type checking
        expected_type = self._get_expected_type(datatype_token)
        actual_type = self._get_actual_type(literal_token)

        # C++ Rule: Strict type matching (no implicit conversions between incompatible types)
        if expected_type != actual_type:
            self.logs.append(f"[ERROR] [SEMANTICS] FATAL ERROR: Type mismatch detected!")
            self.logs.append(f"   Expected: {expected_type}, but got: {actual_type}")
            self.logs.append(f"   Variable '{identifier_token.value}' is declared as '{datatype_token.value}', but value '{literal_token.value}' is {actual_type}.")
            self.logs.append("[SEMANTICS] C++ Rule: No implicit type conversion allowed between incompatible types.")
            self.logs.append("[SEMANTICS] Recovery Strategy: Compiler will discard assignment to prevent memory corruption.")
            self.is_valid = False
        else:
            self.logs.append(f"[SUCCESS] [SEMANTICS] Types match! Expected {expected_type}, got {actual_type}.")
            self.logs.append("[SEMANTICS] C++ Rule: Type compatibility verified - no type coercion needed.")

            # Bind to symbol table
            self.logs.append(f"[SEMANTICS] Binding variable '{identifier_token.value}' to Symbol Table...")
            self.logs.append(f"[SEMANTICS] Scope Level: {self.current_level}, Memory Offset: {self.current_offset}")
            self.symbol_table[identifier_token.value] = {
                'Data Type': datatype_token.value,
                'Level': str(self.current_level),
                'Offset': str(self.current_offset)
            }
            self.logs.append(f"[SUCCESS] [SEMANTICS] Variable '{identifier_token.value}' successfully bound to symbol table.")
            self.logs.append("[SUCCESS] Semantic Analysis Complete.")
            self.is_valid = True

        return self.is_valid, self.logs, self.symbol_table

    def _get_expected_type(self, datatype_token: Token) -> str:
        """Get the expected type category from datatype token."""
        if datatype_token.type == TokenType.DATATYPE_SIGMA:
            return "INTEGER"
        elif datatype_token.type == TokenType.DATATYPE_GYATT:
            return "STRING"
        elif datatype_token.type == TokenType.DATATYPE_SMOL:
            return "FLOAT"
        return "UNKNOWN"

    def _get_actual_type(self, literal_token: Token) -> str:
        """Get the actual type category from literal token following C++ rules."""
        if literal_token.type == TokenType.STRING_LITERAL:
            return "STRING"
        elif literal_token.type == TokenType.NUMERIC_LITERAL:
            # C++ Rule: Strict distinction between int and float
            # - If literal has decimal point -> FLOAT (e.g., 1.0, 3.14)
            # - If literal has no decimal point -> INTEGER (e.g., 1, 100)
            if '.' in literal_token.value:
                return "FLOAT"
            else:
                return "INTEGER"
        elif literal_token.type in [TokenType.TRUE_BET, TokenType.FALSE_COOKED]:
            return "BOOLEAN"
        elif literal_token.type == TokenType.NULL_LIGMA:
            return "NULL"
        return "UNKNOWN"


# ============================================================================
# MULTILINE COMPILER - PROCESSES MULTIPLE STATEMENTS
# ============================================================================
class MultilineCompiler:
    def __init__(self, code: str):
        self.code = code
        self.all_lexer_logs = []
        self.all_parser_logs = []
        self.all_semantic_logs = []
        self.symbol_table = {}
        self.overall_success = True
        self.has_unknown_tokens = False
        self.current_offset = 0  # Track memory offset for symbol table

    def compile(self) -> Tuple[List[str], List[str], List[str], Dict[str, Dict[str, str]], bool, bool]:
        """Compile multiline code and return all logs and symbol table."""

        # Split code into lines and filter out empty lines
        lines = [line.strip() for line in self.code.split('\n') if line.strip()]

        statement_num = 0
        block_depth = 0

        for line_num, line in enumerate(lines, 1):
            # Skip lines that are just braces
            if line == '{':
                block_depth += 1
                self.all_lexer_logs.append(f"[BLOCK] Opening block (depth: {block_depth})")
                self.all_parser_logs.append(f"[BLOCK] Opening block (depth: {block_depth})")
                self.all_semantic_logs.append(f"[BLOCK] Opening block (depth: {block_depth})")
                continue
            elif line == '}':
                block_depth -= 1
                self.all_lexer_logs.append(f"[BLOCK] Closing block (depth: {block_depth})")
                self.all_parser_logs.append(f"[BLOCK] Closing block (depth: {block_depth})")
                self.all_semantic_logs.append(f"[BLOCK] Closing block (depth: {block_depth})")
                continue

            # Process statement
            statement_num += 1
            indent = "  " * block_depth

            # Add statement header (cleaner version)
            self.all_lexer_logs.append(f"\n[STATEMENT #{statement_num}]: {line}")
            self.all_parser_logs.append(f"\n[STATEMENT #{statement_num}]")
            self.all_semantic_logs.append(f"\n[STATEMENT #{statement_num}]")

            # Lexical Analysis
            lexer = Lexer(line)
            tokens, lexer_logs = lexer.tokenize()
            # Filter out the "STARTING" line from lexer
            filtered_lexer_logs = [log for log in lexer_logs if "STARTING" not in log]
            self.all_lexer_logs.extend([f"{indent}{log}" for log in filtered_lexer_logs])

            if lexer.unknown_count > 0:
                self.has_unknown_tokens = True

            # Syntax Analysis
            parser = Parser(tokens)
            syntax_valid, parser_logs = parser.parse()
            # Filter out the "STARTING" line from parser
            filtered_parser_logs = [log for log in parser_logs if "STARTING" not in log]
            self.all_parser_logs.extend([f"{indent}{log}" for log in filtered_parser_logs])

            if not syntax_valid:
                self.overall_success = False

            # Semantic Analysis (with accumulated symbol table)
            semantic_analyzer = SemanticAnalyzer(tokens, current_level=block_depth, current_offset=self.current_offset)
            semantic_analyzer.symbol_table = self.symbol_table.copy()  # Use accumulated table
            semantic_valid, semantic_logs, updated_table = semantic_analyzer.analyze()
            # Filter out the "STARTING" line from semantic analyzer
            filtered_semantic_logs = [log for log in semantic_logs if "STARTING" not in log]
            self.all_semantic_logs.extend([f"{indent}{log}" for log in filtered_semantic_logs])

            # Update symbol table with new variables
            # Check if a new variable was added to increment offset
            new_vars = set(updated_table.keys()) - set(self.symbol_table.keys())
            if new_vars and semantic_valid:
                self.current_offset += 1  # Increment offset for each new variable

            self.symbol_table.update(updated_table)

            if not semantic_valid:
                self.overall_success = False

        # Final summary (cleaner version)
        self.all_lexer_logs.append(f"\n[COMPLETE] Compilation Complete: {statement_num} statement(s) processed")
        self.all_parser_logs.append(f"\n[COMPLETE] Compilation Complete: {statement_num} statement(s) processed")
        self.all_semantic_logs.append(f"\n[COMPLETE] Compilation Complete: {statement_num} statement(s) processed")
        self.all_semantic_logs.append(f"[INFO] Total variables bound: {len(self.symbol_table)}")
        self.all_semantic_logs.append(f"{'='*60}")

        return (self.all_lexer_logs, self.all_parser_logs, self.all_semantic_logs,
                self.symbol_table, self.overall_success, self.has_unknown_tokens)




# ============================================================================
# STREAMLIT UI - THE FRONTEND
# ============================================================================
def main():
    # Page configuration
    st.set_page_config(
        page_title="BRL Compiler",
        layout="wide"
    )

    # Custom CSS for better styling
    st.markdown("""
        <style>
        :root {
            --navy: #0f172a;
            --slate: #1e293b;
            --teal: #0f766e;
            --cyan: #0891b2;
            --amber: #d97706;
            --mint: #10b981;
            --surface: #ffffff;
            --surface-soft: #f8fafc;
            --text: #111827;
            --text-muted: #cbd5e1;
            --border: #e2e8f0;
        }

        /* Main header styling */
        .main-header {
            text-align: center;
            background: linear-gradient(120deg, var(--navy) 0%, var(--teal) 55%, var(--cyan) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 3.5em;
            font-weight: 900;
            margin-bottom: 0.3em;
            letter-spacing: -2px;
        }

        .sub-header {
            text-align: center;
            color: var(--text-muted);
            font-size: 1.3em;
            margin-bottom: 2em;
            font-weight: 500;
        }

        .stApp {
            background: linear-gradient(180deg, var(--navy) 0%, var(--slate) 45%, var(--teal) 100%);
        }

        /* Streamlit component styling */
        .stTextArea textarea {
            font-family: 'Courier New', monospace;
            font-size: 14px;
            border: 2px solid var(--border);
            border-radius: 10px;
            padding: 15px;
            background-color: var(--surface-soft);
            color: var(--text) !important;
        }

        .stTextArea textarea:focus {
            border-color: var(--cyan);
            box-shadow: 0 0 0 0.2rem rgba(8, 145, 178, 0.2);
        }

        /* Ensure placeholder text is visible */
        .stTextArea textarea::placeholder {
            color: var(--text-muted);
            opacity: 0.7;
        }

        /* Button styling */
        .stButton button {
            font-size: 18px;
            font-weight: 700;
            border-radius: 10px;
            padding: 15px 30px;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        }

        /* Column headers */
        .stColumn h3 {
            background: linear-gradient(120deg, var(--navy) 0%, var(--teal) 100%);
            color: white;
            padding: 12px 20px;
            border-radius: 10px 10px 0 0;
            margin-bottom: 0;
            font-weight: 700;
            text-align: center;
        }

        /* Info boxes */
        .element-container div[data-testid="stMarkdownContainer"] p {
            line-height: 1.6;
        }

        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, var(--navy) 0%, var(--slate) 45%, var(--teal) 100%);
            color: white;
        }

        [data-testid="stHeader"],
        [data-testid="stToolbar"],
        [data-testid="stDecoration"] {
            background: linear-gradient(180deg, var(--navy) 0%, var(--slate) 45%, var(--teal) 100%) !important;
            border-bottom: none !important;
            box-shadow: none !important;
        }

        [data-testid="stDecoration"] {
            height: 0 !important;
            min-height: 0 !important;
        }

        [data-testid="stHeader"] button,
        [data-testid="stHeader"] svg,
        [data-testid="stToolbar"] button,
        [data-testid="stToolbar"] svg {
            color: #ffffff !important;
            fill: #ffffff !important;
        }

        [data-testid="stSidebar"] .element-container {
            color: white;
        }

        [data-testid="stSidebar"] h2 {
            color: white;
            font-weight: 700;
            text-align: center;
            margin-bottom: 20px;
        }

        [data-testid="stSidebar"] h3 {
            color: #fbbf24;
            font-weight: 600;
            margin-top: 15px;
        }

        [data-testid="stSidebar"] code {
            background-color: rgba(255, 255, 255, 0.1);
            color: #fff;
            padding: 10px;
            border-radius: 5px;
            display: block;
        }

        /* Success/Error/Warning styling */
        .stSuccess {
            background-color: #d4edda !important;
            border-left: 5px solid var(--mint) !important;
            border-radius: 5px !important;
            padding: 12px !important;
            color: #155724 !important;
        }

        .stError {
            background-color: #f8d7da !important;
            border-left: 5px solid #b91c1c !important;
            border-radius: 5px !important;
            padding: 12px !important;
            color: #721c24 !important;
        }

        .stWarning {
            background-color: #fff3cd !important;
            border-left: 5px solid var(--amber) !important;
            border-radius: 5px !important;
            padding: 12px !important;
            color: #856404 !important;
        }

        .stInfo {
            background-color: #e8f4f8 !important;
            border-left: 5px solid var(--cyan) !important;
            border-radius: 5px !important;
            padding: 12px !important;
            color: #0c5460 !important;
        }

        /* Override Streamlit's default alert styling */
        div[data-testid="stNotification"] {
            background-color: #e8f4f8 !important;
            color: #0c5460 !important;
        }

        div[data-baseweb="notification"] {
            background-color: #e8f4f8 !important;
            color: #0c5460 !important;
        }

        /* Footer styling */
        .footer {
            text-align: center;
            color: var(--text-muted);
            padding: 30px 20px;
            margin-top: 50px;
            border-top: 2px solid var(--border);
        }

        /* Badge styling */
        .badge {
            display: inline-block;
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 14px;
            font-weight: 600;
            margin: 5px;
        }

        .badge-success {
            background-color: #008000;
            color: white;
        }

        .badge-error {
            background-color: #b91c1c;
            color: white;
        }

        .badge-warning {
            background-color: var(--amber);
            color: #000;
        }

        /* Card styling for columns */
        .analysis-card {
            background: var(--surface);
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid var(--border);
        }
        </style>
    """, unsafe_allow_html=True)

    # Header with enhanced styling
    st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <h1 class="main-header">BrainRotLanguage Compiler</h1>
            <p class="sub-header">Structured Code Analysis and Compilation</p>
            <div style='margin: 20px 0;'>
                <span class="badge badge-success">Lexer Ready</span>
                <span class="badge badge-success">Parser Ready</span>
                <span class="badge badge-success">Semantic Checks Ready</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Sidebar: Language Guide with enhanced design
    with st.sidebar:
        st.markdown("<h2>BRL Language Guide</h2>", unsafe_allow_html=True)

        st.markdown("<h3>Data Types</h3>", unsafe_allow_html=True)
        st.code("sigma   → int\ngyatt   → string\nsmol    → float", language="text")

        st.markdown("<h3>Keywords</h3>", unsafe_allow_html=True)
        st.code("rizz    → assignment (=)\nyap     → output\nmogging → input\nchad    → return", language="text")

        st.markdown("<h3>Control Flow</h3>", unsafe_allow_html=True)
        st.code("cap     → if\nflex    → else\ngrind   → while", language="text")

        st.markdown("<h3>Logic Operators</h3>", unsafe_allow_html=True)
        st.code("bussin  → AND\npookie  → OR\ncringe  → NOT", language="text")

        st.markdown("<h3>Fixed Values</h3>", unsafe_allow_html=True)
        st.code("bet     → true\ncooked  → false\nligma   → null", language="text")

        st.markdown("<h3>Delimiter</h3>", unsafe_allow_html=True)
        st.code("!   → end of statement", language="text")

        st.divider()
        st.markdown("<h3>Example Code</h3>", unsafe_allow_html=True)
        st.code("""sigma points rizz 100!
smol health rizz 95.5!
{
gyatt rank rizz "S-Tier"!
sigma ammo rizz 30!
}""", language="text")

    # Main Input with enhanced design
    st.markdown("---")
    st.markdown("<h2 style='text-align: center; color: #0f766e;'>Enter Your BRL Code</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #cbd5e1; margin-bottom: 20px;'>Write your BrainRotLanguage code below and hit compile!</p>", unsafe_allow_html=True)

    code_input = st.text_area(
        "Code Input",
        placeholder="""Example:
sigma points rizz 100!
smol health rizz 95.5!
{
gyatt rank rizz "S-Tier"!
sigma ammo rizz 30!
}""",
        label_visibility="collapsed",
        height=250
    )

    # Compile button with enhanced styling
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        compile_button = st.button("[COMPILE CODE]", type="primary", use_container_width=True)

    # Quick Tips Section
    with st.expander("Quick Tips & Examples"):
        st.markdown("""
        ### How to Use:
        1. **Write your BRL code** in the text area above
        2. **Click the "COMPILE CODE" button**
        3. **Watch the magic happen!** See your code analyzed in real-time

        ### Example Codes to Try:

        **Basic Variable Declaration:**
        ```
        sigma age rizz 25!
        ```

        **Multiple Variables:**
        ```
        sigma playerID rizz 101!
        smol healthPos rizz 98.5!
        gyatt username rizz "ProGamer"!
        ```

        **With Block Structure:**
        ```
        sigma points rizz 100!
        smol health rizz 95.5!
        {
        gyatt rank rizz "S-Tier"!
        sigma ammo rizz 30!
        }
        ```

        ### Test Error Handling:

        **Type Mismatch (Will Fail):**
        ```
        sigma age rizz "Twenty"!
        ```

        **Missing Delimiter (Will Fail):**
        ```
        sigma age rizz 20
        ```

        **Unknown Token (Panic Mode):**
        ```
        sigma age @@ 20!
        ```
        """)

    st.markdown("---")

    st.markdown("---")

    # Welcome message when no compilation has happened yet
    if not compile_button:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #008000 0%, #008000 100%);
                        padding: 40px; border-radius: 15px; text-align: center;
                        box-shadow: 0 8px 16px rgba(0,0,0,0.2); margin: 30px 0;'>
                <h2 style='color: white; margin: 0; font-size: 2.5em;'>Welcome to BRL Compiler</h2>
                <p style='color: white; font-size: 1.2em; margin-top: 15px; line-height: 1.6;'>
                    Ready to compile code?<br>
                    Write your BrainRotLanguage source above and click <strong>"COMPILE CODE"</strong> to start analysis.
                </p>
                
            </div>

            <div style='text-align: center; margin-top: 30px;'>
                <h3 style='color: #0f766e;'>Features</h3>
                <div style='display: flex; justify-content: space-around; margin-top: 20px; flex-wrap: wrap;'>
                    <div style='flex: 1; min-width: 200px; padding: 20px;'>
                        <h4>Lexical Analysis</h4>
                        <p>Tokenizes your code and identifies each component</p>
                    </div>
                    <div style='flex: 1; min-width: 200px; padding: 20px;'>
                        <h4>Syntax Analysis</h4>
                        <p>Validates grammar structure and statement rules</p>
                    </div>
                    <div style='flex: 1; min-width: 200px; padding: 20px;'>
                        <h4>Semantic Analysis</h4>
                        <p>Checks types and binds variables to symbol table</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    if compile_button and code_input:
        st.markdown("---")
        st.markdown("<h2 style='text-align: center; color: #0f766e; margin-bottom: 30px;'>Compilation Results</h2>", unsafe_allow_html=True)

        # Use MultilineCompiler for processing
        compiler = MultilineCompiler(code_input)
        lexer_logs, parser_logs, semantic_logs, symbol_table, overall_success, has_unknown = compiler.compile()

        # Quick Stats Dashboard
        statement_count = len([line for line in code_input.split('\n') if line.strip() and line.strip() not in ['{', '}']])

        status_value = "PASS" if overall_success else "FAIL"
        status_accent = "#10b981" if overall_success else "#dc3545"

        token_value = "WARN" if has_unknown else "CLEAN"
        token_accent = "#d97706" if has_unknown else "#0891b2"

        stats_html = (
            "<div style='display:flex;justify-content:center;gap:18px;flex-wrap:wrap;margin:10px 0 6px 0;'>"
            f"<div style='background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);border:1px solid #0f766e;border-radius:12px;min-height:140px;width:290px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;box-shadow:0 8px 16px rgba(0,0,0,0.25);'><h3 style='color:#ffffff;margin:0;font-size:2em;line-height:1.1;'>{statement_count}</h3><p style='color:#cbd5e1;margin:10px 0 0 0;font-size:1.2em;'>Statements</p></div>"
            f"<div style='background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);border:1px solid #10b981;border-radius:12px;min-height:140px;width:290px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;box-shadow:0 8px 16px rgba(0,0,0,0.25);'><h3 style='color:#ffffff;margin:0;font-size:2em;line-height:1.1;'>{len(symbol_table)}</h3><p style='color:#cbd5e1;margin:10px 0 0 0;font-size:1.2em;'>Variables</p></div>"
            f"<div style='background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);border:1px solid {status_accent};border-radius:12px;min-height:140px;width:290px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;box-shadow:0 8px 16px rgba(0,0,0,0.25);'><h3 style='color:#ffffff;margin:0;font-size:2em;line-height:1.1;'>{status_value}</h3><p style='color:#cbd5e1;margin:10px 0 0 0;font-size:1.2em;'>Status</p></div>"
            f"<div style='background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%);border:1px solid {token_accent};border-radius:12px;min-height:140px;width:290px;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;box-shadow:0 8px 16px rgba(0,0,0,0.25);'><h3 style='color:#ffffff;margin:0;font-size:2em;line-height:1.1;'>{token_value}</h3><p style='color:#cbd5e1;margin:10px 0 0 0;font-size:1.2em;'>Tokens</p></div>"
            "</div>"
        )
        st.markdown(stats_html, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Use Streamlit tabs for analysis results
        st.markdown("<h2 style='text-align: center; color: #0f766e; margin: 20px 0;'>Analysis Results</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #cbd5e1; margin-bottom: 20px;'>Click on a tab to view the analysis details</p>", unsafe_allow_html=True)

        def render_log_row(log: str) -> None:
            """Render compiler logs with a unified black background."""
            border_color = "#475569"
            if "[ERROR]" in log or "FATAL" in log or "ERROR" in log:
                border_color = "#dc3545"
            elif "[WARNING]" in log or "Unknown" in log:
                border_color = "#d97706"
            elif "[SUCCESS]" in log:
                border_color = "#0f766e"
            elif "[STATEMENT #" in log:
                border_color = "#0f766e"
            elif "[BLOCK]" in log or "[INFO]" in log:
                border_color = "#0891b2"

            safe_log = html.escape(log)
            st.markdown(
                (
                    "<div style='background: #000000; color: #ffffff; padding: 8px 12px; "
                    "border-radius: 6px; margin: 8px 0; font-family: monospace; "
                    f"border-left: 4px solid {border_color};'>{safe_log}</div>"
                ),
                unsafe_allow_html=True,
            )

        tab1, tab2, tab3, tab4 = st.tabs(["Lexical Analysis", "Syntax Analysis", "Semantic Analysis", "Symbol Table"])

        with tab1:
            st.markdown("""
                <div style='background: linear-gradient(135deg, #0f766e 0%, #0f766e 100%);
                            padding: 15px; border-radius: 10px 10px 0 0;'>
                    <h3 style='color: white; margin: 0; text-align: center;'>🔍 LEXICAL ANALYSIS</h3>
                </div>
            """, unsafe_allow_html=True)
            with st.container(height=400):
                for log in lexer_logs:
                    if not log.strip():
                        continue
                    render_log_row(log)

        with tab2:
            st.markdown("""
                <div style='background: linear-gradient(135deg, #0f766e 0%, #0f766e 100%);
                            padding: 15px; border-radius: 10px 10px 0 0;'>
                    <h3 style='color: white; margin: 0; text-align: center;'>SYNTAX ANALYSIS</h3>
                </div>
            """, unsafe_allow_html=True)
            with st.container(height=400):
                for log in parser_logs:
                    if not log.strip():
                        continue
                    render_log_row(log)

        with tab3:
            st.markdown("""
                <div style='background: linear-gradient(135deg, #0f766e 0%, #0f766e 100%);
                            padding: 15px; border-radius: 10px 10px 0 0;'>
                    <h3 style='color: white; margin: 0; text-align: center;'>SEMANTIC ANALYSIS</h3>
                </div>
            """, unsafe_allow_html=True)
            with st.container(height=400):
                for log in semantic_logs:
                    if not log.strip():
                        continue
                    render_log_row(log)

        with tab4:
            st.markdown("""
                <div style='background: linear-gradient(135deg, #0f766e 0%, #0f766e 100%);
                            padding: 15px; border-radius: 10px 10px 0 0;'>
                    <h3 style='color: white; margin: 0; text-align: center;'>SYMBOL TABLE</h3>
                </div>
            """, unsafe_allow_html=True)

            if symbol_table:
                st.markdown(f"<p style='text-align: center; color: #0f766e; font-size: 18px; font-weight: 600; margin: 15px 0;'>{len(symbol_table)} Variables Bound</p>", unsafe_allow_html=True)
                df = pd.DataFrame.from_dict(symbol_table, orient='index')
                df.index.name = 'Variable'
                df.reset_index(inplace=True)

                # Reorder columns to ensure proper display: Variable, Data Type, Level, Offset
                df = df[['Variable', 'Data Type', 'Level', 'Offset']]

                # Display the dataframe with custom styling
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                    height=350
                )
            else:
                st.info("No variables bound yet. The symbol table will populate after successful compilation.")

        # Overall Status with enhanced design
        st.markdown("---")
        st.markdown("<h2 style='text-align: center; color: #0f766e; margin: 30px 0;'>Compilation Status</h2>", unsafe_allow_html=True)

        if not has_unknown and overall_success:
            st.markdown("""
                <div style='background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
                            padding: 30px; border-radius: 15px; text-align: center;
                            box-shadow: 0 8px 16px rgba(0,0,0,0.2);'>
                    <h1 style='color: white; margin: 0; font-size: 2.5em;'>COMPILATION SUCCESSFUL</h1>
                    <p style='color: white; font-size: 1.3em; margin-top: 10px;'>
                        All analysis phases completed with no errors.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        elif has_unknown:
            st.markdown("""
                <div style='background: linear-gradient(135deg, #ffc107 0%, #ff9800 100%);
                            padding: 30px; border-radius: 15px; text-align: center;
                            box-shadow: 0 8px 16px rgba(0,0,0,0.2);'>
                    <h1 style='color: white; margin: 0; font-size: 2.5em;'>COMPILATION COMPLETED WITH WARNINGS</h1>
                    <p style='color: white; font-size: 1.3em; margin-top: 10px;'>
                        Unknown tokens were detected and skipped through panic-mode recovery.
                    </p>
                </div>
            """, unsafe_allow_html=True)
        elif not overall_success:
            st.markdown("""
                <div style='background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
                            padding: 30px; border-radius: 15px; text-align: center;
                            box-shadow: 0 8px 16px rgba(0,0,0,0.2);'>
                    <h1 style='color: white; margin: 0; font-size: 2.5em;'>COMPILATION ERRORS</h1>
                    <p style='color: white; font-size: 1.3em; margin-top: 10px;'>
                        Errors were found. Review the logs above for details.
                    </p>
                </div>
            """, unsafe_allow_html=True)

    elif compile_button and not code_input:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        padding: 40px; border-radius: 15px; text-align: center;
                        box-shadow: 0 8px 16px rgba(0,0,0,0.2); margin-top: 30px;'>
                <h2 style='color: white; margin: 0; font-size: 2em;'>Input Required</h2>
                <p style='color: white; font-size: 1.2em; margin-top: 10px;'>
                    Enter BRL source code before compiling.
                </p>
            </div>
        """, unsafe_allow_html=True)

    # Footer with enhanced styling
    st.markdown("---")
    st.markdown("""
        <div class='footer'>
            <h3 style='color: #0f766e; margin-bottom: 15px;'>BrainRotLanguage Compiler</h3>
            <p style='font-size: 16px; margin: 10px 0;'>
                Built for <strong>CS Programming Languages Final Project</strong>
            </p>
            <p style='font-size: 14px; color: #aaa; margin: 5px 0;'>
                <em>Version 2.0 with multiline compilation support</em>
            </p>
            <p style='font-size: 14px; color: #aaa;'>
                <em>Designed for readable diagnostics and fast feedback</em>
            </p>
            <div style='margin-top: 20px;'>
                <span class="badge badge-success">Lexer</span>
                <span class="badge badge-success">Parser</span>
                <span class="badge badge-success">Semantic Analyzer</span>
                <span class="badge badge-warning">Panic Mode</span>
            </div>
        </div>
    """, unsafe_allow_html=True)


# ============================================================================
# RUN THE APP
# ============================================================================
if __name__ == "__main__":
    main()
