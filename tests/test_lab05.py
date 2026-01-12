"""
Lab 05: Scoring & Ranking - Auto-grading Tests
"""

import pytest
import os
import nbformat

# Get paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NOTEBOOK_PATH = os.path.join(BASE_DIR, 'exercise', 'Lab05_Exercise.ipynb')


@pytest.fixture(scope="session")
def student_namespace():
    """Execute student notebook and return namespace with variables."""
    
    with open(NOTEBOOK_PATH, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    
    namespace = {'__name__': '__main__'}
    
    original_dir = os.getcwd()
    exercise_dir = os.path.join(BASE_DIR, 'exercise')
    os.chdir(exercise_dir)
    
    try:
        for cell in nb.cells:
            if cell.cell_type == 'code':
                if '# Quick check' in cell.source or '# Verification' in cell.source:
                    continue
                try:
                    exec(cell.source, namespace)
                except Exception as e:
                    print(f"Cell execution warning: {e}")
    finally:
        os.chdir(original_dir)
    
    return namespace


# ============== Exercise 1: Calculate Score (25 points) ==============

def test_ex1_get_score_exists(student_namespace):
    """Test that get_score function exists"""
    assert 'get_score' in student_namespace, "Function 'get_score' not found"


def test_ex1_get_score_callable(student_namespace):
    """Test that get_score is callable"""
    assert callable(student_namespace.get('get_score')), "'get_score' should be a function"


def test_ex1_get_score_finds_matches(student_namespace):
    """Test that get_score finds matches"""
    func = student_namespace.get('get_score')
    if func:
        assert func('fever', 'fever and high fever') == 2, "get_score('fever', 'fever and high fever') should return 2"


def test_ex1_get_score_no_match(student_namespace):
    """Test that get_score returns 0 when no match"""
    func = student_namespace.get('get_score')
    if func:
        assert func('rash', 'no match here') == 0, "get_score('rash', 'no match here') should return 0"


# ============== Exercise 2: Sort Documents by Score (25 points) ==============

def test_ex2_sorted_docs_exists(student_namespace):
    """Test that sorted_docs variable exists"""
    assert 'sorted_docs' in student_namespace, "Variable 'sorted_docs' not found"


def test_ex2_sorted_docs_is_list(student_namespace):
    """Test that sorted_docs is a list"""
    assert isinstance(student_namespace.get('sorted_docs'), list), "'sorted_docs' should be a list"


def test_ex2_sorted_docs_order(student_namespace):
    """Test that sorted_docs is in correct order"""
    sorted_docs = student_namespace.get('sorted_docs', [])
    if len(sorted_docs) >= 3:
        assert sorted_docs[0]['score'] == 3, "First item should have score 3"
        assert sorted_docs[1]['score'] == 2, "Second item should have score 2"
        assert sorted_docs[2]['score'] == 1, "Third item should have score 1"


# ============== Exercise 3: Top-K Function (25 points) ==============

def test_ex3_top_k_exists(student_namespace):
    """Test that top_k function exists"""
    assert 'top_k' in student_namespace, "Function 'top_k' not found"


def test_ex3_top_k_callable(student_namespace):
    """Test that top_k is callable"""
    assert callable(student_namespace.get('top_k')), "'top_k' should be a function"


def test_ex3_top_k_works(student_namespace):
    """Test that top_k works correctly"""
    func = student_namespace.get('top_k')
    if func:
        assert func([1, 2, 3, 4, 5], 3) == [1, 2, 3], "top_k([1, 2, 3, 4, 5], 3) should return [1, 2, 3]"


def test_ex3_top_k_strings(student_namespace):
    """Test that top_k works with strings"""
    func = student_namespace.get('top_k')
    if func:
        assert func(['a', 'b', 'c'], 2) == ['a', 'b'], "top_k(['a', 'b', 'c'], 2) should return ['a', 'b']"


# ============== Exercise 4: Search and Rank (25 points) ==============

def test_ex4_search_rank_exists(student_namespace):
    """Test that search_rank function exists"""
    assert 'search_rank' in student_namespace, "Function 'search_rank' not found"


def test_ex4_search_rank_callable(student_namespace):
    """Test that search_rank is callable"""
    assert callable(student_namespace.get('search_rank')), "'search_rank' should be a function"


def test_ex4_search_rank_returns_list(student_namespace):
    """Test that search_rank returns a list"""
    func = student_namespace.get('search_rank')
    documents = student_namespace.get('documents', [])
    if func and documents:
        result = func('fever', documents, 2)
        assert isinstance(result, list), "search_rank should return a list"


def test_ex4_search_rank_correct_count(student_namespace):
    """Test that search_rank returns correct count"""
    func = student_namespace.get('search_rank')
    documents = student_namespace.get('documents', [])
    if func and documents:
        result = func('fever', documents, 2)
        assert len(result) == 2, f"search_rank should return 2 results, got {len(result)}"


def test_ex4_search_rank_sorted(student_namespace):
    """Test that search_rank results are sorted"""
    func = student_namespace.get('search_rank')
    documents = student_namespace.get('documents', [])
    if func and documents:
        result = func('fever', documents, 2)
        if len(result) >= 2:
            assert result[0]['score'] >= result[1]['score'], "Results should be sorted by score descending"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
