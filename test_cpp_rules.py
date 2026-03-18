#!/usr/bin/env python3
"""
Comprehensive C++ Rules Test for BRL Compiler
Tests Parser (Syntax) and Semantic Analysis C++ compliance
"""

from brl_compiler import MultilineCompiler

def test_parser_rules():
    """Test Parser C++ Syntax Rules"""
    print('='*80)
    print('PARSER (SYNTAX ANALYSIS) - C++ RULES TEST')
    print('='*80)
    print()

    test_cases = {
        'VALID SYNTAX': [
            ('sigma age rizz 100!', 'Basic valid statement'),
            ('smol health rizz 95.5!', 'Float assignment'),
            ('gyatt name rizz "John"!', 'String assignment'),
        ],

        'INVALID SYNTAX - EXTRA TOKENS': [
            ('sigma age rizz 100! extra', 'Extra token after delimiter'),
            ('sigma age rizz 100! 200!', 'Multiple values after delimiter'),
        ],

        'INVALID SYNTAX - MISSING TOKENS': [
            ('sigma age rizz', 'Missing delimiter'),
            ('sigma age', 'Missing assignment and value'),
            ('sigma', 'Missing identifier, assignment, value, delimiter'),
        ],

        'INVALID SYNTAX - WRONG ORDER': [
            ('age sigma rizz 100!', 'Identifier before datatype'),
            ('sigma rizz age 100!', 'Assignment before identifier'),
        ],
    }

    for category, cases in test_cases.items():
        print(f'{category}:')
        print('-'*80)
        for code, description in cases:
            compiler = MultilineCompiler(code)
            _, parser_logs, _, _, overall_success, _ = compiler.compile()

            has_error = any('ERROR' in log for log in parser_logs)

            if 'INVALID' in category:
                if has_error:
                    print(f'  PASS: {description:40} -> Correctly rejected')
                else:
                    print(f'  FAIL: {description:40} -> Should be rejected!')
            else:
                if not has_error:
                    print(f'  PASS: {description:40} -> Correctly accepted')
                else:
                    print(f'  FAIL: {description:40} -> Should be accepted!')
        print()


def test_semantic_rules():
    """Test Semantic Analysis C++ Rules"""
    print('='*80)
    print('SEMANTIC ANALYSIS - C++ RULES TEST')
    print('='*80)
    print()

    test_cases = {
        'VALID SEMANTICS - TYPE MATCHING': [
            ('sigma age rizz 100!', 'Integer to sigma (int)'),
            ('smol health rizz 95.5!', 'Float to smol (float)'),
            ('gyatt name rizz "John"!', 'String to gyatt (string)'),
        ],

        'INVALID SEMANTICS - TYPE MISMATCH': [
            ('sigma age rizz "Twenty"!', 'String to sigma (int) - MISMATCH'),
            ('smol health rizz "95.5"!', 'String to smol (float) - MISMATCH'),
            ('gyatt name rizz 100!', 'Integer to gyatt (string) - MISMATCH'),
        ],

        'INVALID SEMANTICS - STRICT INT/FLOAT': [
            ('sigma age rizz 100.0!', 'Float literal to sigma (int) - STRICT'),
            ('smol health rizz 95!', 'Integer literal to smol (float) - STRICT'),
        ],

        'INVALID SEMANTICS - REDECLARATION (SAME SCOPE)': [
            ('sigma age rizz 100!\nsigma age rizz 200!', 'Redeclare in same scope (Level 0)'),
            ('{\nsigma x rizz 1!\nsigma x rizz 2!\n}', 'Redeclare in same block (Level 1)'),
        ],

        'VALID SEMANTICS - SHADOWING (DIFFERENT SCOPE)': [
            ('sigma age rizz 100!\n{\nsigma age rizz 200!\n}', 'Shadow outer variable - ALLOWED'),
        ],
    }

    for category, cases in test_cases.items():
        print(f'{category}:')
        print('-'*80)
        for code, description in cases:
            compiler = MultilineCompiler(code)
            _, _, semantic_logs, _, overall_success, _ = compiler.compile()

            has_error = any('FATAL ERROR' in log for log in semantic_logs)
            has_warning = any('WARNING' in log for log in semantic_logs)

            if 'INVALID' in category:
                if has_error:
                    print(f'  PASS: {description:50} -> Correctly rejected')
                else:
                    print(f'  FAIL: {description:50} -> Should be rejected!')
            elif 'SHADOWING' in category:
                if has_warning and not has_error:
                    print(f'  PASS: {description:50} -> Warning issued, allowed')
                else:
                    print(f'  FAIL: {description:50} -> Should warn but allow!')
            else:
                if not has_error:
                    print(f'  PASS: {description:50} -> Correctly accepted')
                else:
                    print(f'  FAIL: {description:50} -> Should be accepted!')
        print()


def test_comprehensive_example():
    """Test comprehensive example with all rules"""
    print('='*80)
    print('COMPREHENSIVE EXAMPLE - ALL C++ RULES')
    print('='*80)
    print()

    code = '''sigma points rizz 100!
smol health rizz 95.5!
{
gyatt rank rizz "S-Tier"!
sigma ammo rizz 30!
}
sigma final rizz 5000!'''

    print('Code:')
    print('-'*80)
    print(code)
    print('-'*80)
    print()

    compiler = MultilineCompiler(code)
    lexer_logs, parser_logs, semantic_logs, symbol_table, overall_success, has_unknown = compiler.compile()

    print('Results:')
    print(f'  Overall Success: {overall_success}')
    print(f'  Has Unknown Tokens: {has_unknown}')
    print(f'  Variables Bound: {len(symbol_table)}')
    print()

    print('Symbol Table:')
    print('-'*80)
    for var, info in symbol_table.items():
        print(f"  {var:15} | Type: {info['Data Type']:6} | Level: {info['Level']} | Offset: {info['Offset']}")
    print('-'*80)
    print()

    if overall_success and not has_unknown and len(symbol_table) == 5:
        print('PASS: Comprehensive example compiled successfully!')
    else:
        print('FAIL: Comprehensive example has issues!')
    print()


if __name__ == '__main__':
    test_parser_rules()
    print('\n\n')
    test_semantic_rules()
    print('\n\n')
    test_comprehensive_example()

    print('='*80)
    print('ALL TESTS COMPLETE!')
    print('='*80)
