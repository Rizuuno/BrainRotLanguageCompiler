"""
BRL Compiler - Quick Test Script
Run this to verify everything works before submission!
"""

from brl_compiler import Lexer, Parser, SemanticAnalyzer, MultilineCompiler

def test_single_line():
    """Test 1: Single line valid code"""
    print("\n" + "="*60)
    print("TEST 1: Single Line Valid Code")
    print("="*60)
    code = "sigma age rizz 20!"
    print(f"Code: {code}")

    lexer = Lexer(code)
    tokens, _ = lexer.tokenize()

    parser = Parser(tokens)
    syntax_valid, _ = parser.parse()

    semantic = SemanticAnalyzer(tokens)
    semantic_valid, _, table = semantic.analyze()

    print(f"Tokens: {len(tokens)}")
    print(f"Syntax Valid: {syntax_valid}")
    print(f"Semantic Valid: {semantic_valid}")
    print(f"Symbol Table: {table}")

    assert len(tokens) == 5, "Should have 5 tokens"
    assert syntax_valid, "Syntax should be valid"
    assert semantic_valid, "Semantics should be valid"
    assert 'age' in table, "Variable 'age' should be in table"

    print("[PASS] TEST 1 PASSED!")
    return True


def test_multiline():
    """Test 2: Multiline code"""
    print("\n" + "="*60)
    print("TEST 2: Multiline Code")
    print("="*60)
    code = """sigma playerID rizz 101!
smol healthPos rizz 98.5!
gyatt rank rizz "S-Tier"!
sigma finalScore rizz 5000!"""

    print(f"Code:\n{code}\n")

    compiler = MultilineCompiler(code)
    _, _, _, table, success, has_unknown = compiler.compile()

    print(f"Compilation Success: {success}")
    print(f"Has Unknown Tokens: {has_unknown}")
    print(f"Variables in Table: {len(table)}")
    print(f"Symbol Table: {list(table.keys())}")

    assert success, "Compilation should succeed"
    assert not has_unknown, "Should have no unknown tokens"
    assert len(table) == 4, "Should have 4 variables"

    print("[PASS] TEST 2 PASSED!")
    return True


def test_type_mismatch():
    """Test 3: Type mismatch error"""
    print("\n" + "="*60)
    print("TEST 3: Type Mismatch Error")
    print("="*60)
    code = 'sigma age rizz "Twenty"!'
    print(f"Code: {code}")

    lexer = Lexer(code)
    tokens, _ = lexer.tokenize()

    parser = Parser(tokens)
    syntax_valid, _ = parser.parse()

    semantic = SemanticAnalyzer(tokens)
    semantic_valid, _, table = semantic.analyze()

    print(f"Syntax Valid: {syntax_valid}")
    print(f"Semantic Valid: {semantic_valid}")
    print(f"Symbol Table: {table}")

    assert syntax_valid, "Syntax should be valid"
    assert not semantic_valid, "Semantics should FAIL (type mismatch)"
    assert len(table) == 0, "No variables should be bound"

    print("[PASS] TEST 3 PASSED!")
    return True


def test_missing_delimiter():
    """Test 4: Missing delimiter"""
    print("\n" + "="*60)
    print("TEST 4: Missing Delimiter")
    print("="*60)
    code = "sigma age rizz 20"
    print(f"Code: {code}")

    lexer = Lexer(code)
    tokens, _ = lexer.tokenize()

    parser = Parser(tokens)
    syntax_valid, _ = parser.parse()

    print(f"Tokens: {len(tokens)}")
    print(f"Syntax Valid: {syntax_valid}")

    assert len(tokens) == 4, "Should have 4 tokens (missing delimiter)"
    assert not syntax_valid, "Syntax should FAIL (missing delimiter)"

    print("[PASS] TEST 4 PASSED!")
    return True


def test_unknown_token():
    """Test 5: Unknown token (Panic Mode)"""
    print("\n" + "="*60)
    print("TEST 5: Unknown Token (Panic Mode)")
    print("="*60)
    code = "sigma age @@ 20!"
    print(f"Code: {code}")

    lexer = Lexer(code)
    tokens, _ = lexer.tokenize()

    print(f"Tokens: {len(tokens)}")
    print(f"Unknown Count: {lexer.unknown_count}")

    assert lexer.unknown_count > 0, "Should have unknown tokens"

    print("[PASS] TEST 5 PASSED!")
    return True


def test_block_structure():
    """Test 6: Block structure"""
    print("\n" + "="*60)
    print("TEST 6: Block Structure")
    print("="*60)
    code = """sigma playerID rizz 101!
smol healthPos rizz 98.5!
{
    gyatt rank rizz "S-Tier"!
    sigma ammoCount rizz 30!
}
sigma finalScore rizz 5000!"""

    print(f"Code:\n{code}\n")

    compiler = MultilineCompiler(code)
    _, _, _, table, success, has_unknown = compiler.compile()

    print(f"Compilation Success: {success}")
    print(f"Variables in Table: {len(table)}")
    print(f"Symbol Table: {list(table.keys())}")

    assert success, "Compilation should succeed"
    assert len(table) == 5, "Should have 5 variables"
    assert 'rank' in table, "Variable 'rank' should be in table"

    print("[PASS] TEST 6 PASSED!")
    return True


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print(" BRL COMPILER - AUTOMATED TEST SUITE")
    print("="*70)

    tests = [
        test_single_line,
        test_multiline,
        test_type_mismatch,
        test_missing_delimiter,
        test_unknown_token,
        test_block_structure
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            if test():
                passed += 1
        except AssertionError as e:
            print(f"[FAIL] TEST FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"[ERROR] TEST ERROR: {e}")
            failed += 1

    print("\n" + "="*70)
    print(f" TEST RESULTS: {passed} Passed, {failed} Failed")
    print("="*70)

    if failed == 0:
        print("\n*** ALL TESTS PASSED! Your compiler is ready for submission! ***\n")
        print("Next steps:")
        print("1. Run: streamlit run brl_compiler.py")
        print("2. Capture screenshots")
        print("3. Record video demo")
        print("4. Package and submit!")
    else:
        print(f"\n*** WARNING: {failed} test(s) failed. Please review the errors above. ***\n")

    return failed == 0


if __name__ == "__main__":
    run_all_tests()
