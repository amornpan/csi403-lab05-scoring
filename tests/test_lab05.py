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


class TestExercise1:
    """Test Exercise 1: Calculate Score (25 points)"""
    
    def test_get_score_exists(self, student_namespace):
        assert 'get_score' in student_namespace, "Function 'get_score' not found"
    
    def test_get_score_callable(self, student_namespace):
        assert callable(student_namespace.get('get_score')), "'get_score' should be a function"
    
    def test_get_score_finds_matches(self, student_namespace):
        func = student_namespace.get('get_score')
        if func:
            assert func('fever', 'fever and high fever') == 2, "get_score('fever', 'fever and high fever') should return 2"
    
    def test_get_score_no_match(self, student_namespace):
        func = student_namespace.get('get_score')
        if func:
            assert func('rash', 'no match here') == 0, "get_score('rash', 'no match here') should return 0"


class TestExercise2:
    """Test Exercise 2: Sort Documents by Score (25 points)"""
    
    def test_sorted_docs_exists(self, student_namespace):
        assert 'sorted_docs' in student_namespace, "Variable 'sorted_docs' not found"
    
    def test_sorted_docs_is_list(self, student_namespace):
        assert isinstance(student_namespace.get('sorted_docs'), list), "'sorted_docs' should be a list"
    
    def test_sorted_docs_order(self, student_namespace):
        sorted_docs = student_namespace.get('sorted_docs', [])
        if len(sorted_docs) >= 3:
            assert sorted_docs[0]['score'] == 3, "First item should have score 3"
            assert sorted_docs[1]['score'] == 2, "Second item should have score 2"
            assert sorted_docs[2]['score'] == 1, "Third item should have score 1"


class TestExercise3:
    """Test Exercise 3: Top-K Function (25 points)"""
    
    def test_top_k_exists(self, student_namespace):
        assert 'top_k' in student_namespace, "Function 'top_k' not found"
    
    def test_top_k_callable(self, student_namespace):
        assert callable(student_namespace.get('top_k')), "'top_k' should be a function"
    
    def test_top_k_works(self, student_namespace):
        func = student_namespace.get('top_k')
        if func:
            assert func([1, 2, 3, 4, 5], 3) == [1, 2, 3], "top_k([1, 2, 3, 4, 5], 3) should return [1, 2, 3]"
    
    def test_top_k_strings(self, student_namespace):
        func = student_namespace.get('top_k')
        if func:
            assert func(['a', 'b', 'c'], 2) == ['a', 'b'], "top_k(['a', 'b', 'c'], 2) should return ['a', 'b']"


class TestExercise4:
    """Test Exercise 4: Search and Rank (25 points)"""
    
    def test_search_rank_exists(self, student_namespace):
        assert 'search_rank' in student_namespace, "Function 'search_rank' not found"
    
    def test_search_rank_callable(self, student_namespace):
        assert callable(student_namespace.get('search_rank')), "'search_rank' should be a function"
    
    def test_search_rank_returns_list(self, student_namespace):
        func = student_namespace.get('search_rank')
        documents = student_namespace.get('documents', [])
        if func and documents:
            result = func('fever', documents, 2)
            assert isinstance(result, list), "search_rank should return a list"
    
    def test_search_rank_correct_count(self, student_namespace):
        func = student_namespace.get('search_rank')
        documents = student_namespace.get('documents', [])
        if func and documents:
            result = func('fever', documents, 2)
            assert len(result) == 2, f"search_rank should return 2 results, got {len(result)}"
    
    def test_search_rank_sorted(self, student_namespace):
        func = student_namespace.get('search_rank')
        documents = student_namespace.get('documents', [])
        if func and documents:
            result = func('fever', documents, 2)
            if len(result) >= 2:
                assert result[0]['score'] >= result[1]['score'], "Results should be sorted by score descending"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
