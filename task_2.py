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

class TestFunctionalThreatScores(unittest.TestCase):

    def test_all_departments_have_high_scores(self):
        """All departments have high average scores, expecting a high aggregated score."""
        departments = [
            generate_random_data(80, 5, 50),
            generate_random_data(85, 5, 60),
            generate_random_data(82, 5, 40),
            generate_random_data(83, 5, 70),
        ]
        department_scores = [calculate_department_threat_score(dept) for dept in departments]
        result = aggregate_user_threat_score(department_scores)
        self.assertTrue(80 <= result <= 90)

    def test_some_departments_have_low_scores(self):
        """Some departments have very low scores while others have high scores, expecting a high threat score overall."""
        departments = [
            generate_random_data(80, 5, 50),
            generate_random_data(85, 5, 60),
            generate_random_data(20, 5, 40),
            generate_random_data(15, 5, 70),
        ]
        department_scores = [calculate_department_threat_score(dept) for dept in departments]
        result = aggregate_user_threat_score(department_scores)
        self.assertTrue(50 <= result <= 90)

    def test_one_department_has_extreme_outliers(self):
        """All departments have the same mean threat score, but one department has extreme outliers."""
        departments = [
            generate_random_data(30, 5, 50),
            generate_random_data(30, 5, 60),
            generate_random_data(30, 5, 40),
            np.append(generate_random_data(30, 5, 70), [90, 90, 90]), 
        ]
        department_scores = [calculate_department_threat_score(dept) for dept in departments]
        result = aggregate_user_threat_score(department_scores)
        self.assertTrue(30 <= result <= 90)

    def test_departments_with_different_number_of_users(self):
        """Departments have varying numbers of users, but aggregation still works."""
        departments = [
            generate_random_data(30, 5, 10),  
            generate_random_data(40, 5, 100), 
            generate_random_data(50, 5, 60), 
            generate_random_data(60, 5, 30),  
        ]
        department_scores = [calculate_department_threat_score(dept) for dept in departments]
        result = aggregate_user_threat_score(department_scores)
        self.assertTrue(30 <= result <= 90)

if __name__ == "__main__":
    unittest.main()
