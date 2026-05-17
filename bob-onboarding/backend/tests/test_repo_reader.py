"""
Unit tests for repository reader module.
Tests cloning, file reading, binary detection, and cleanup.
"""
import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
import subprocess

from backend.repo_reader import (
    clone_and_read,
    is_binary_file,
    should_ignore_path,
    extract_repo_name,
    RepoReaderError
)


def test_extract_repo_name():
    """Test repository name extraction from URL."""
    url = "https://github.com/octocat/Hello-World"
    result = extract_repo_name(url)
    assert result == "octocat_Hello-World"


def test_extract_repo_name_with_git_suffix():
    """Test repository name extraction with .git suffix."""
    url = "https://github.com/octocat/Hello-World.git"
    result = extract_repo_name(url)
    assert result == "octocat_Hello-World"


def test_extract_repo_name_invalid_url():
    """Test error handling for invalid URL."""
    with pytest.raises(RepoReaderError) as exc_info:
        extract_repo_name("https://github.com/invalid")
    
    assert "Invalid GitHub URL" in str(exc_info.value)


def test_is_binary_file_text():
    """Test binary detection for text files."""
    # Create temporary text file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("This is a text file")
        temp_path = Path(f.name)
    
    try:
        assert not is_binary_file(temp_path)
    finally:
        temp_path.unlink()


def test_is_binary_file_binary():
    """Test binary detection for binary files."""
    # Create temporary binary file with null bytes
    with tempfile.NamedTemporaryFile(mode='wb', suffix='.bin', delete=False) as f:
        f.write(b'\x00\x01\x02\x03')
        temp_path = Path(f.name)
    
    try:
        assert is_binary_file(temp_path)
    finally:
        temp_path.unlink()


def test_should_ignore_path_node_modules():
    """Test that node_modules is ignored."""
    base = Path("/repo")
    path = Path("/repo/node_modules/package/file.js")
    assert should_ignore_path(path, base)


def test_should_ignore_path_git():
    """Test that .git directory is ignored."""
    base = Path("/repo")
    path = Path("/repo/.git/config")
    assert should_ignore_path(path, base)


def test_should_ignore_path_pycache():
    """Test that __pycache__ is ignored."""
    base = Path("/repo")
    path = Path("/repo/src/__pycache__/module.pyc")
    assert should_ignore_path(path, base)


def test_should_ignore_path_env_file():
    """Test that .env files are ignored."""
    base = Path("/repo")
    path = Path("/repo/.env")
    assert should_ignore_path(path, base)


def test_should_ignore_path_lock_files():
    """Test that lock files are ignored."""
    base = Path("/repo")
    assert should_ignore_path(Path("/repo/package-lock.json"), base)
    assert should_ignore_path(Path("/repo/yarn.lock"), base)
    assert should_ignore_path(Path("/repo/poetry.lock"), base)


def test_should_ignore_path_allowed_files():
    """Test that normal files are not ignored."""
    base = Path("/repo")
    assert not should_ignore_path(Path("/repo/src/main.py"), base)
    assert not should_ignore_path(Path("/repo/README.md"), base)
    assert not should_ignore_path(Path("/repo/.gitignore"), base)


def test_clone_and_read_invalid_url():
    """Test error for non-GitHub URL."""
    with pytest.raises(RepoReaderError) as exc_info:
        clone_and_read("https://gitlab.com/user/repo")
    
    assert "must start with 'https://github.com/'" in str(exc_info.value)


@patch('subprocess.run')
def test_clone_and_read_nonexistent_repo(mock_run):
    """Test handling of 404 repository not found."""
    mock_run.return_value = MagicMock(
        returncode=128,
        stderr="fatal: repository 'https://github.com/nonexistent/repo' not found"
    )
    
    with pytest.raises(RepoReaderError) as exc_info:
        clone_and_read("https://github.com/nonexistent/repo")
    
    assert "Git clone failed" in str(exc_info.value)


@patch('subprocess.run')
def test_clone_and_read_success(mock_run):
    """Test successful repository cloning and reading."""
    # Create a temporary directory structure
    temp_dir = tempfile.mkdtemp()
    repo_dir = Path(temp_dir) / "test_repo"
    repo_dir.mkdir()
    
    # Create test files
    (repo_dir / "README.md").write_text("# Test Repo")
    (repo_dir / "src").mkdir()
    (repo_dir / "src" / "main.py").write_text("print('hello')")
    
    # Mock successful git clone
    mock_run.return_value = MagicMock(returncode=0, stderr="")
    
    try:
        with patch('tempfile.mkdtemp', return_value=temp_dir):
            with patch('backend.repo_reader.extract_repo_name', return_value='test_repo'):
                result = clone_and_read("https://github.com/test/repo")
                
                assert len(result) == 2
                assert "README.md" in result
                assert "src/main.py" in result or "src\\main.py" in result
                assert "# Test Repo" in result["README.md"]
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


@patch('subprocess.run')
def test_clone_and_read_max_chars_per_file(mock_run):
    """Test file content truncation."""
    temp_dir = tempfile.mkdtemp()
    repo_dir = Path(temp_dir) / "test_repo"
    repo_dir.mkdir()
    
    # Create a large file
    large_content = "x" * 5000
    (repo_dir / "large.txt").write_text(large_content)
    
    mock_run.return_value = MagicMock(returncode=0, stderr="")
    
    try:
        with patch('tempfile.mkdtemp', return_value=temp_dir):
            with patch('backend.repo_reader.extract_repo_name', return_value='test_repo'):
                result = clone_and_read("https://github.com/test/repo", max_chars_per_file=100)
                
                assert "large.txt" in result
                assert len(result["large.txt"]) == 100
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


@patch('subprocess.run')
def test_clone_and_read_cleanup_temp_directory(mock_run):
    """Test cleanup of temporary directory after success."""
    temp_dir = tempfile.mkdtemp()
    repo_dir = Path(temp_dir) / "test_repo"
    repo_dir.mkdir()
    (repo_dir / "file.txt").write_text("test")
    
    mock_run.return_value = MagicMock(returncode=0, stderr="")
    
    with patch('tempfile.mkdtemp', return_value=temp_dir):
        with patch('backend.repo_reader.extract_repo_name', return_value='test_repo'):
            clone_and_read("https://github.com/test/repo")
    
    # Verify temp directory was cleaned up
    assert not Path(temp_dir).exists()


@patch('subprocess.run')
def test_clone_and_read_cleanup_on_failure(mock_run):
    """Test cleanup of temporary directory after failure."""
    temp_dir = tempfile.mkdtemp()
    
    mock_run.return_value = MagicMock(
        returncode=128,
        stderr="fatal: error"
    )
    
    with patch('tempfile.mkdtemp', return_value=temp_dir):
        with pytest.raises(RepoReaderError):
            clone_and_read("https://github.com/test/repo")
    
    # Verify temp directory was cleaned up even on failure
    assert not Path(temp_dir).exists()


@patch('subprocess.run')
def test_clone_timeout(mock_run):
    """Test timeout handling during clone."""
    mock_run.side_effect = subprocess.TimeoutExpired('git', 120)
    
    with pytest.raises(RepoReaderError) as exc_info:
        clone_and_read("https://github.com/test/repo")
    
    assert "timed out" in str(exc_info.value)


@patch('subprocess.run')
def test_clone_and_read_empty_repo(mock_run):
    """Test handling of empty repository."""
    temp_dir = tempfile.mkdtemp()
    repo_dir = Path(temp_dir) / "test_repo"
    repo_dir.mkdir()
    # No files created - empty repo
    
    mock_run.return_value = MagicMock(returncode=0, stderr="")
    
    try:
        with patch('tempfile.mkdtemp', return_value=temp_dir):
            with patch('backend.repo_reader.extract_repo_name', return_value='test_repo'):
                with pytest.raises(RepoReaderError) as exc_info:
                    clone_and_read("https://github.com/test/repo")
                
                assert "No readable files found" in str(exc_info.value)
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

# Made with Bob
