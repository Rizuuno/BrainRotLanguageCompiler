#!/usr/bin/env python3
"""
Comprehensive Syntax and Semantic Analysis Test for BRL Compiler
Tests all C++ syntax and semantic rules implementation
"""

from brl_compiler import MultilineCompiler

def print_section(title):
    """Print a formatted section header."""
    print('\n' + '='*80)
    print(f'{title:^80}')
    print('='*80 + '\n')

def test_case(name, code, expected_result):
    """Run a single test case."""
    print(f'TEST: {name}')
    print(f'CODE: {code}')
    compiler = MultilineCompiler(code)
    lexer_logs, parser_logs, semantic_logs, symbol_table, overall_success, has_unknown = compiler.compile()

    result = 'PASS' if overall_success == expected_result['success'] else 'FAIL'
    print(f'RESULT: {result}')
    print(f'  - Overall Success: {overall_success} (Expected: {expected_result["success"]})')
    print(f'  - Has Unknown Tokens: {has_unknown}')
    print(f'  - Variables Bound: {len(symbol_table)}')

    if result == 'FAIL':
        print('  PARSER LOGS:')
        for log in parser_logs:
            if 'ERROR' in log or '❌' in log:
                print(f'    {log}')
        print('  SEMANTIC LOGS:')
        for log in semantic_logs:
            if 'ERROR' in log or '❌' in log:
                print(f'    {log}')
    print('-'*80)

    return result == 'PASS'

def main():
    print_section('BRL COMPILER - SYNTAX & SEMANTIC ANALYSIS TEST SUITE')
    print('Testing C++ compliance for Parser and Semantic Analyzer')

    passed = 0
    failed = 0

    # ========================================================================
    # SYNTAX ANALYSIS TESTS
    # ========================================================================
    print_section('SYNTAX ANALYSIS TESTS (C++ RULES)')

    # Test 1: Valid statement structure
    if test_case(
        'Valid Statement - Correct Structure',
        'sigma age rizz 100!',
        {'success': True}
    ): passed += 1
    else: failed += 1

    # Test 2: Missing delimiter
    if test_case(
        'Missing Delimiter - Syntax Error',
        'sigma age rizz 100',
        {'success': False}
    ): passed += 1
    else: failed += 1

    # Test 3: Extra tokens after delimiter
    if test_case(
        'Extra Tokens - Syntax Error',
        'sigma age rizz 100 200!',
        {'success': False}
    ): passed += 1
    else: failed += 1

    # Test 4: Missing datatype
    if test_case(
        'Missing Datatype - Syntax Error',
        'age rizz 100!',
        {'success': False}
    ): passed += 1
    else: failed += 1

    # Test 5: Missing identifier
    if test_case(
        'Missing Identifier - Syntax Error',
        'sigma rizz 100!',
        {'success': False}
    ): passed += 1
    else: failed += 1

    # Test 6: Missing assign operator
    if test_case(
        'Missing Assignment Operator - Syntax Error',
        'sigma age 100!',
        {'success': False}
    ): passed += 1
    else: failed += 1

    # Test 7: Invalid identifier (keyword as variable name)
    if test_case(
        'Keyword as Identifier - Syntax Error',
        'sigma sigma rizz 100!',
        {'success': False}
    ): passed += 1
    else: failed += 1

    # ========================================================================
    # SEMANTIC ANALYSIS TESTS - TYPE CHECKING
    # ========================================================================
    print_section('SEMANTIC ANALYSIS TESTS - TYPE CHECKING (C++ RULES)')

    # Test 8: Valid integer assignment
    if test_case(
        'Valid Integer Assignment',
        'sigma count rizz 42!',
        {'success': True}
    ): passed += 1
    else: failed += 1

    # Test 9: Valid float assignment
    if test_case(
        'Valid Float Assignment',
        'smol temp rizz 98.6!',
        {'success': True}
    ): passed += 1
    else: failed += 1

    # Test 10: Valid string assignment
    if test_case(
        'Valid String Assignment',
        'gyatt name rizz "John"!',
        {'success': True}
    ): passed += 1
    else: failed += 1

    # Test 11: Type mismatch - sigma with string
    if test_case(
        'Type Mismatch - INTEGER expects STRING',
        'sigma age rizz "Twenty"!',
        {'success': False}
    ): passed += 1
    else: failed += 1

    # Test 12: Type mismatch - gyatt with number
    if test_case(
        'Type Mismatch - STRING expects INTEGER',
        'gyatt name rizz 123!',
        {'success': False}
    ): passed += 1
    else: failed += 1

    # Test 13: Type mismatch - smol with string
    if test_case(
        'Type Mismatch - FLOAT expects STRING',
        'smol ratio rizz "3.14"!',
        {'success': False}
    ): passed += 1
    else: failed += 1

    # Test 14: Strict int/float distinction - sigma with float
    if test_case(
        'Type Mismatch - INTEGER expects FLOAT (C++ strict)',
        'sigma count rizz 100.0!',
        {'success': False}
    ): passed += 1
    else: failed += 1

    # Test 15: Strict int/float distinction - smol with int
    if test_case(
        'Type Mismatch - FLOAT expects INTEGER (C++ strict)',
        'smol temp rizz 100!',
        {'success': False}
    ): passed += 1
    else: failed += 1

    # ========================================================================
    # SEMANTIC ANALYSIS TESTS - VARIABLE REDECLARATION
    # ========================================================================
    print_section('SEMANTIC ANALYSIS TESTS - REDECLARATION (C++ RULES)')

    # Test 16: Variable redeclaration in same scope
    if test_case(
        'Redeclaration in Same Scope - Semantic Error',
        '''sigma x rizz 100!
sigma x rizz 200!''',
        {'success': False}
    ): passed += 1
    else: failed += 1

    # Test 17: Variable shadowing in nested scope (allowed)
    if test_case(
        'Variable Shadowing - Different Scope (Allowed)',
        '''sigma x rizz 100!
{
sigma x rizz 200!
}''',
        {'success': True}
    ): passed += 1
    else: failed += 1

    # Test 18: Multiple variables in same scope (no redeclaration)
    if test_case(
        'Multiple Different Variables - Same Scope (Valid)',
        '''sigma x rizz 100!
sigma y rizz 200!
sigma z rizz 300!''',
        {'success': True}
    ): passed += 1
    else: failed += 1

    # ========================================================================
    # COMBINED TESTS - LEXICAL + SYNTAX + SEMANTIC
    # ========================================================================
    print_section('COMBINED TESTS - ALL PHASES')

    # Test 19: Invalid identifier (starts with digit)
    if test_case(
        'Invalid Identifier - Lexical Error',
        'sigma 1age rizz 100!',
        {'success': False}
    ): passed += 1
    else: failed += 1

    # Test 20: Complex valid program with blocks
    if test_case(
        'Complex Valid Program - All Phases',
        '''sigma points rizz 100!
smol health rizz 95.5!
{
gyatt rank rizz "S-Tier"!
sigma ammo rizz 30!
}''',
        {'success': True}
    ): passed += 1
    else: failed += 1

    # Test 21: Multiple errors (missing delimiter + type mismatch)
    if test_case(
        'Multiple Errors - Syntax and Semantic',
        '''sigma age rizz 100
sigma name rizz 456!''',
        {'success': False}
    ): passed += 1
    else: failed += 1

    # Test 22: Unknown token with valid statement
    if test_case(
        'Unknown Token - Lexical Panic Mode',
        'sigma age @@ 100!',
        {'success': False}
    ): passed += 1
    else: failed += 1

    # ========================================================================
    # FINAL RESULTS
    # ========================================================================
    print_section('TEST RESULTS SUMMARY')

    total = passed + failed
    percentage = (passed / total * 100) if total > 0 else 0

    print(f'Total Tests: {total}')
    print(f'Passed: {passed}')
    print(f'Failed: {failed}')
    print(f'Success Rate: {percentage:.1f}%')
    print()

    if failed == 0:
        print('✅ ALL TESTS PASSED! BRL Compiler is C++ compliant!')
    else:
        print(f'❌ {failed} TEST(S) FAILED. Review implementation.')

    print('='*80)

if __name__ == '__main__':
    main()
