import numpy as np
import unittest

# Utility Functions
def generate_random_data(mean, variance, num_samples):
    """Generates random threat scores for a given mean, variance, and sample size."""
    return np.random.randint(max(mean - variance, 0), min(mean + variance + 1, 90), num_samples)

def calculate_department_threat_score(threat_scores, importance):
    """Calculates the weighted average threat score for a department, based on its importance."""
    department_avg = np.mean(threat_scores)
    return department_avg * importance

def aggregate_user_threat_score(department_scores, total_importance):
    """Calculates the final aggregated threat score for the company by normalizing weighted averages."""
    weighted_sum = sum(department_scores)
    # Normalize by total importance to bring the score within the 0-90 range.
    return min(weighted_sum / total_importance, 90)

# Unit Test and Functional Test Case Class
class TestAggregatedThreatScore(unittest.TestCase):

    def test_generate_random_data(self):
        """Test if generated threat scores are within the expected range."""
        data = generate_random_data(mean=30, variance=10, num_samples=50)
        self.assertTrue((data >= 0).all() and (data <= 90).all())

    def test_calculate_department_threat_score(self):
        """Test calculation of department threat score with a sample list of scores and importance."""
        threat_scores = [10, 20, 30, 40, 50]
        importance = 3
        department_score = calculate_department_threat_score(threat_scores, importance)
        self.assertAlmostEqual(department_score, 90, delta=0.1)

    def test_aggregate_user_threat_score(self):
        """Test the final aggregation of department threat scores."""
        department_scores = [90, 60, 30]
        total_importance = 5
        aggregate_score = aggregate_user_threat_score(department_scores, total_importance)
        self.assertAlmostEqual(aggregate_score, 36, delta=0.1)

    # Functional Test Cases

    def test_equal_department_importance_similar_threats(self):
        """Test scenario with similar threat levels and equal importance across departments."""
        departments = [
            generate_random_data(30, 5, 50),
            generate_random_data(32, 5, 50),
            generate_random_data(28, 5, 50),
            generate_random_data(31, 5, 50),
            generate_random_data(29, 5, 50)
        ]
        importance = [3, 3, 3, 3, 3]
        department_scores = [calculate_department_threat_score(dept, imp) for dept, imp in zip(departments, importance)]
        total_importance = sum(importance)
        result = aggregate_user_threat_score(department_scores, total_importance)
        self.assertTrue(0 <= result <= 90)

    def test_different_importance_levels(self):
        """Test varying department importance levels."""
        departments = [
            generate_random_data(50, 10, 100),
            generate_random_data(20, 5, 150),
            generate_random_data(15, 5, 120),
            generate_random_data(10, 3, 50),
            generate_random_data(35, 8, 80)
        ]
        importance = [5, 4, 3, 2, 4]
        department_scores = [calculate_department_threat_score(dept, imp) for dept, imp in zip(departments, importance)]
        total_importance = sum(importance)
        result = aggregate_user_threat_score(department_scores, total_importance)
        self.assertTrue(0 <= result <= 90)

    def test_high_outliers_in_one_department(self):
        """Test handling of outliers in one department's threat scores."""
        departments = [
            generate_random_data(10, 3, 100),
            generate_random_data(15, 4, 120),
            generate_random_data(20, 5, 100),
            generate_random_data(70, 10, 50),
            generate_random_data(12, 3, 80)
        ]
        importance = [3, 3, 3, 5, 3]
        department_scores = [calculate_department_threat_score(dept, imp) for dept, imp in zip(departments, importance)]
        total_importance = sum(importance)
        result = aggregate_user_threat_score(department_scores, total_importance)
        self.assertTrue(0 <= result <= 90)

    def test_minimal_threats_in_all_departments(self):
        """Test case where all departments have minimal threat scores."""
        departments = [
            generate_random_data(5, 2, 100),
            generate_random_data(5, 2, 120),
            generate_random_data(5, 2, 80),
            generate_random_data(5, 2, 60),
            generate_random_data(5, 2, 90)
        ]
        importance = [2, 3, 2, 3, 2]
        department_scores = [calculate_department_threat_score(dept, imp) for dept, imp in zip(departments, importance)]
        total_importance = sum(importance)
        result = aggregate_user_threat_score(department_scores, total_importance)
        self.assertTrue(0 <= result <= 90)

if __name__ == "__main__":
    unittest.main()
