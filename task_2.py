import numpy as np
import unittest
import os
import pandas as pd

# Utility Functions (same as before)
def generate_random_data(mean, variance, num_samples):
    """Generates random threat scores for a given mean, variance, and sample size."""
    return np.random.randint(max(mean - variance, 0), min(mean + variance + 1, 90), num_samples)

def save_to_csv(data, filename):
    """Save data to a CSV file."""
    pd.DataFrame(data).to_csv(filename, index=False, header=False)

def read_from_csv(filename):
    """Read data from a CSV file."""
    return pd.read_csv(filename, header=None).to_numpy().flatten()

def generate_or_read_data(filename, mean, variance, num_samples):
    """Generate data if CSV does not exist, otherwise read from CSV."""
    if os.path.exists(filename):
        print(f"Reading data from {filename}")
        return read_from_csv(filename)
    else:
        print(f"Generating new data and saving to {filename}")
        data = generate_random_data(mean, variance, num_samples)
        save_to_csv(data, filename)
        return data

# Updated Test Cases
class TestFunctionalThreatScoresWithCSV(unittest.TestCase):

    def test_all_departments_same_mean(self):
        """All departments have the same mean threat score."""
        department_files = ["dept1_same_mean.csv", "dept2_same_mean.csv", "dept3_same_mean.csv"]
        departments = [
            generate_or_read_data(department_files[0], mean=50, variance=10, num_samples=50),
            generate_or_read_data(department_files[1], mean=50, variance=10, num_samples=60),
            generate_or_read_data(department_files[2], mean=50, variance=10, num_samples=70),
        ]
        department_scores = [np.mean(dept) for dept in departments]
        result = min(np.mean(department_scores), 90)
        self.assertTrue(40 <= result <= 60)

    def test_one_department_high_mean(self):
        """One department has a much higher mean score than the others."""
        department_files = ["dept1_high_mean.csv", "dept2_low_mean.csv"]
        departments = [
            generate_or_read_data(department_files[0], mean=80, variance=5, num_samples=50),
            generate_or_read_data(department_files[1], mean=30, variance=5, num_samples=60),
        ]
        department_scores = [np.mean(dept) for dept in departments]
        result = min(np.mean(department_scores), 90)
        self.assertTrue(50 <= result <= 80)

    def test_high_variance_in_one_department(self):
        """One department has high variance in threat scores."""
        department_files = ["dept1_high_variance.csv", "dept2_low_variance.csv"]
        departments = [
            generate_or_read_data(department_files[0], mean=50, variance=30, num_samples=50),
            generate_or_read_data(department_files[1], mean=50, variance=5, num_samples=60),
        ]
        department_scores = [np.mean(dept) for dept in departments]
        result = min(np.mean(department_scores), 90)
        self.assertTrue(40 <= result <= 70)

    def test_different_user_counts(self):
        """Departments have different numbers of users."""
        department_files = ["dept1_diff_users.csv", "dept2_diff_users.csv", "dept3_diff_users.csv"]
        departments = [
            generate_or_read_data(department_files[0], mean=50, variance=10, num_samples=10),
            generate_or_read_data(department_files[1], mean=50, variance=10, num_samples=100),
            generate_or_read_data(department_files[2], mean=50, variance=10, num_samples=60),
        ]
        department_scores = [np.mean(dept) for dept in departments]
        result = min(np.mean(department_scores), 90)
        self.assertTrue(40 <= result <= 60)

    def test_empty_department(self):
        """Test case where one department has no users (empty department)."""
        department_files = ["dept1_empty.csv", "dept2_non_empty.csv"]
        departments = [
            generate_or_read_data(department_files[0], mean=50, variance=10, num_samples=0),  # Empty department
            generate_or_read_data(department_files[1], mean=50, variance=10, num_samples=50),
        ]
        department_scores = [np.mean(dept) for dept in departments if dept.size > 0]
        result = min(np.mean(department_scores), 90) if department_scores else 0
        self.assertEqual(result, 0)

    def test_single_department(self):
        """Test case where only one department is included."""
        department_files = ["dept_single.csv"]
        departments = [
            generate_or_read_data(department_files[0], mean=50, variance=10, num_samples=50),
        ]
        department_scores = [np.mean(dept) for dept in departments]
        result = min(np.mean(department_scores), 90)
        self.assertTrue(40 <= result <= 60)

    def test_all_maximum_scores(self):
        """Test case where all departments have maximum possible threat scores."""
        department_files = ["dept1_max.csv", "dept2_max.csv", "dept3_max.csv"]
        departments = [
            generate_or_read_data(department_files[0], mean=85, variance=5, num_samples=50),
            generate_or_read_data(department_files[1], mean=90, variance=0, num_samples=50),
            generate_or_read_data(department_files[2], mean=90, variance=0, num_samples=50),
        ]
        department_scores = [np.mean(dept) for dept in departments]
        result = min(np.mean(department_scores), 90)
        self.assertEqual(result, 90)

    def test_all_minimum_scores(self):
        """Test case where all departments have minimum possible threat scores."""
        department_files = ["dept1_min.csv", "dept2_min.csv", "dept3_min.csv"]
        departments = [
            generate_or_read_data(department_files[0], mean=5, variance=2, num_samples=50),
            generate_or_read_data(department_files[1], mean=0, variance=0, num_samples=50),
            generate_or_read_data(department_files[2], mean=5, variance=2, num_samples=50),
        ]
        department_scores = [np.mean(dept) for dept in departments]
        result = min(np.mean(department_scores), 90)
        self.assertEqual(result, 0)

    def test_extreme_variance_across_departments(self):
        """Test case with extreme variance across departments."""
        department_files = ["dept1_extreme.csv", "dept2_extreme.csv"]
        departments = [
            generate_or_read_data(department_files[0], mean=50, variance=40, num_samples=50),
            generate_or_read_data(department_files[1], mean=50, variance=5, num_samples=60),
        ]
        department_scores = [np.mean(dept) for dept in departments]
        result = min(np.mean(department_scores), 90)
        self.assertTrue(40 <= result <= 70)

    def test_one_high_scoring_user(self):
        """One department has a single high-scoring user."""
        department_files = ["dept1_high_user.csv", "dept2_normal.csv"]
        departments = [
            generate_or_read_data(department_files[0], mean=30, variance=5, num_samples=49) + [90],  # One high user
            generate_or_read_data(department_files[1], mean=50, variance=10, num_samples=50),
        ]
        department_scores = [np.mean(dept) for dept in departments]
        result = min(np.mean(department_scores), 90)
        self.assertTrue(50 <= result <= 90)

    def test_one_empty_department(self):
        """Test case where one department is empty."""
        department_files = ["dept1.csv", "dept_empty.csv"]
        departments = [
            generate_or_read_data(department_files[0], mean=50, variance=10, num_samples=50),
            generate_or_read_data(department_files[1], mean=50, variance=10, num_samples=0),  # Empty department
        ]
        department_scores = [np.mean(dept) for dept in departments if dept.size > 0]
        result = min(np.mean(department_scores), 90) if department_scores else 0
        self.assertEqual(result, 0)

    def test_large_user_count(self):
        """Test case where a department has a large number of users."""
        department_files = ["dept_large.csv"]
        departments = [
            generate_or_read_data(department_files[0], mean=50, variance=10, num_samples=1000),
        ]
        department_scores = [np.mean(dept) for dept in departments]
        result = min(np.mean(department_scores), 90)
        self.assertTrue(40 <= result <= 60)

    def test_small_user_count(self):
        """Test case where a department has a small number of users."""
        department_files = ["dept_small.csv"]
        departments = [
            generate_or_read_data(department_files[0], mean=50, variance=10, num_samples=10),
        ]
        department_scores = [np.mean(dept) for dept in departments]
        result = min(np.mean(department_scores), 90)
        self.assertTrue(40 <= result <= 60)

    def test_mixed_distributions(self):
        """Test case with mixed distributions of threat scores across departments."""
        department_files = ["dept_mixed1.csv", "dept_mixed2.csv"]
        departments = [
            generate_or_read_data(department_files[0], mean=80, variance=5, num_samples=30),
            generate_or_read_data(department_files[1], mean=30, variance=20, num_samples=60),
        ]
        department_scores = [np.mean(dept) for dept in departments]
        result = min(np.mean(department_scores), 90)
        self.assertTrue(40 <= result <= 80)

    def test_highest_possible_variance(self):
        """Test case with the highest possible variance in one department."""
        department_files = ["dept_highest_variance.csv"]
        departments = [
            generate_or_read_data(department_files[0], mean=50, variance=45, num_samples=50),
        ]
        department_scores = [np.mean(dept) for dept in departments]
        result = min(np.mean(department_scores), 90)
        self.assertTrue(40 <= result <= 70)

    def test_extreme_low_mean(self):
        """Test case with an extremely low mean in one department."""
        department_files = ["dept_low_mean.csv"]
        departments = [
            generate_or_read_data(department_files[0], mean=5, variance=2, num_samples=50),
        ]
        department_scores = [np.mean(dept) for dept in departments]
        result = min(np.mean(department_scores), 90)
        self.assertTrue(0 <= result <= 10)

    def test_extreme_high_mean(self):
        """Test case with an extremely high mean in one department."""
        department_files = ["dept_high_mean.csv"]
        departments = [
            generate_or_read_data(department_files[0], mean=85, variance=5, num_samples=50),
        ]
        department_scores = [np.mean(dept) for dept in departments]
        result = min(np.mean(department_scores), 90)
        self.assertTrue(80 <= result <= 90)

    def test_two_departments_identical_high_variance(self):
        """Test case with two departments having identical high variance."""
        department_files = ["dept1_identical_variance.csv", "dept2_identical_variance.csv"]
        departments = [
            generate_or_read_data(department_files[0], mean=50, variance=30, num_samples=50),
            generate_or_read_data(department_files[1], mean=50, variance=30, num_samples=50),
        ]
        department_scores = [np.mean(dept) for dept in departments]
        result = min(np.mean(department_scores), 90)
        self.assertTrue(40 <= result <= 70)

    def test_high_and_low_variance_combined(self):
        """Test case where one department has high variance and another has low variance."""
        department_files = ["dept_high_low_variance.csv", "dept_low_variance.csv"]
        departments = [
            generate_or_read_data(department_files[0], mean=50, variance=30, num_samples=50),
            generate_or_read_data(department_files[1], mean=50, variance=5, num_samples=50),
        ]
        department_scores = [np.mean(dept) for dept in departments]
        result = min(np.mean(department_scores), 90)
        self.assertTrue(40 <= result <= 70)

    def test_one_department_all_max_scores(self):
        """Test case where one department has all users scoring maximum scores."""
        department_files = ["dept_max_score.csv"]
        departments = [
            generate_or_read_data(department_files[0], mean=90, variance=0, num_samples=50),
        ]
        department_scores = [np.mean(dept) for dept in departments]
        result = min(np.mean(department_scores), 90)
        self.assertEqual(result, 90)

    def test_one_department_all_min_scores(self):
        """Test case where one department has all users scoring minimum scores."""
        department_files = ["dept_min_score.csv"]
        departments = [
            generate_or_read_data(department_files[0], mean=0, variance=0, num_samples=50),
        ]
        department_scores = [np.mean(dept) for dept in departments]
        result = min(np.mean(department_scores), 90)
        self.assertEqual(result, 0)
    
    def test_one_department_many_users_high_mean(self):
        """Test case where one department has many users and a high mean score."""
        department_files = ["dept_many_users_high.csv"]
        departments = [
            generate_or_read_data(department_files[0], mean=85, variance=5, num_samples=200),
        ]
        department_scores = [np.mean(dept) for dept in departments]
        result = min(np.mean(department_scores), 90)
        self.assertTrue(80 <= result <= 90)

    def test_high_scores_fewer_users(self):
        """Test case where fewer users contribute high scores."""
        department_files = ["dept_few_users_high.csv"]
        departments = [
            generate_or_read_data(department_files[0], mean=85, variance=5, num_samples=20),
        ]
        department_scores = [np.mean(dept) for dept in departments]
        result = min(np.mean(department_scores), 90)
        self.assertTrue(80 <= result <= 90)

    def test_low_scores_fewer_users(self):
        """Test case where fewer users contribute low scores."""
        department_files = ["dept_few_users_low.csv"]
        departments = [
            generate_or_read_data(department_files[0], mean=5, variance=2, num_samples=20),
        ]
        department_scores = [np.mean(dept) for dept in departments]
        result = min(np.mean(department_scores), 90)
        self.assertTrue(0 <= result <= 10)

if __name__ == "__main__":
    unittest.main()
