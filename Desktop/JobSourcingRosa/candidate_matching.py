"""
Candidate Matching System
Matches candidates with suitable positions based on their profile and preferences
"""

import json
import re
from datetime import datetime
from typing import List, Dict, Tuple

class CandidateMatcher:
    def __init__(self):
        self.jobs_file = "edjoin_jobs.json"
        self.candidates_file = "candidates.json"
        self.matches_file = "candidate_matches.json"
    
    def load_jobs(self) -> List[Dict]:
        """Load job positions from JSON file"""
        try:
            with open(self.jobs_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def load_candidates(self) -> List[Dict]:
        """Load candidate profiles from JSON file"""
        try:
            with open(self.candidates_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def save_candidate(self, candidate_data: Dict) -> str:
        """Save new candidate profile"""
        candidates = self.load_candidates()
        candidate_id = f"candidate_{len(candidates) + 1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        candidate_data['id'] = candidate_id
        candidate_data['created_at'] = datetime.now().isoformat()
        candidate_data['status'] = 'active'
        
        candidates.append(candidate_data)
        
        with open(self.candidates_file, 'w', encoding='utf-8') as f:
            json.dump(candidates, f, indent=2, ensure_ascii=False)
        
        return candidate_id
    
    def calculate_match_score(self, candidate: Dict, job: Dict) -> float:
        """Calculate compatibility score between candidate and job (0-100)"""
        score = 0.0
        max_score = 100.0
        
        # Role preference matching (40 points)
        candidate_roles = [role.lower().strip() for role in candidate.get('preferred_roles', [])]
        job_role = job.get('role', '').lower()
        
        if job_role in candidate_roles:
            score += 40.0
        elif any(role in job_role for role in candidate_roles):
            score += 30.0
        elif any(job_role in role for role in candidate_roles):
            score += 25.0
        
        # Location preference matching (25 points)
        candidate_locations = [loc.lower().strip() for loc in candidate.get('preferred_locations', [])]
        job_location = job.get('location', '').lower()
        
        if any(loc in job_location for loc in candidate_locations):
            score += 25.0
        elif any(job_location in loc for loc in candidate_locations):
            score += 20.0
        elif not candidate_locations:  # No location preference
            score += 15.0
        
        # Experience level matching (20 points)
        candidate_experience = candidate.get('years_experience', 0)
        job_title = job.get('title', '').lower()
        
        # Director/Assistant Director roles typically need 5+ years
        if 'director' in job_title and candidate_experience >= 5:
            score += 20.0
        elif 'assistant director' in job_title and candidate_experience >= 3:
            score += 20.0
        elif 'dean' in job_title and candidate_experience >= 7:
            score += 20.0
        elif 'principal' in job_title and candidate_experience >= 5:
            score += 20.0
        elif candidate_experience >= 3:
            score += 15.0
        
        # Education level matching (10 points)
        candidate_education = candidate.get('education_level', '').lower()
        if 'phd' in candidate_education or 'doctorate' in candidate_education:
            score += 10.0
        elif 'master' in candidate_education:
            score += 8.0
        elif 'bachelor' in candidate_education:
            score += 6.0
        
        # Skills matching (5 points)
        candidate_skills = [skill.lower().strip() for skill in candidate.get('skills', [])]
        job_title_lower = job.get('title', '').lower()
        
        skill_keywords = ['curriculum', 'student', 'academic', 'leadership', 'management', 'education']
        matching_skills = sum(1 for skill in skill_keywords if skill in job_title_lower and skill in candidate_skills)
        score += min(matching_skills * 2, 5.0)
        
        return min(score, max_score)
    
    def find_matches(self, candidate_id: str = None, min_score: float = 60.0) -> List[Dict]:
        """Find job matches for a candidate or all candidates"""
        jobs = self.load_jobs()
        candidates = self.load_candidates()
        
        if candidate_id:
            candidates = [c for c in candidates if c.get('id') == candidate_id]
        
        matches = []
        
        for candidate in candidates:
            if candidate.get('status') != 'active':
                continue
                
            candidate_matches = []
            
            for job in jobs:
                score = self.calculate_match_score(candidate, job)
                
                if score >= min_score:
                    match = {
                        'candidate_id': candidate.get('id'),
                        'candidate_name': candidate.get('name'),
                        'candidate_email': candidate.get('email'),
                        'job_id': job.get('url', '').split('/')[-1],
                        'job_title': job.get('title'),
                        'job_role': job.get('role'),
                        'job_location': job.get('location'),
                        'job_url': job.get('url'),
                        'match_score': round(score, 1),
                        'matched_at': datetime.now().isoformat()
                    }
                    candidate_matches.append(match)
            
            # Sort by match score (highest first)
            candidate_matches.sort(key=lambda x: x['match_score'], reverse=True)
            matches.extend(candidate_matches)
        
        # Save matches
        with open(self.matches_file, 'w', encoding='utf-8') as f:
            json.dump(matches, f, indent=2, ensure_ascii=False)
        
        return matches
    
    def get_candidate_matches(self, candidate_id: str) -> List[Dict]:
        """Get matches for a specific candidate"""
        matches = self.load_matches()
        return [match for match in matches if match.get('candidate_id') == candidate_id]
    
    def load_matches(self) -> List[Dict]:
        """Load saved matches"""
        try:
            with open(self.matches_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def get_top_candidates_for_job(self, job_url: str, limit: int = 5) -> List[Dict]:
        """Get top candidates for a specific job"""
        matches = self.load_matches()
        job_matches = [match for match in matches if match.get('job_url') == job_url]
        job_matches.sort(key=lambda x: x['match_score'], reverse=True)
        return job_matches[:limit]

def main():
    """Test the candidate matching system"""
    matcher = CandidateMatcher()
    
    # Create sample candidate
    sample_candidate = {
        'name': 'John Smith',
        'email': 'john.smith@email.com',
        'phone': '555-0123',
        'years_experience': 8,
        'education_level': 'Master of Education',
        'preferred_roles': ['Director', 'Assistant Director'],
        'preferred_locations': ['Los Angeles', 'San Francisco'],
        'skills': ['curriculum', 'leadership', 'management', 'student services'],
        'resume_url': 'uploads/john_smith_resume.pdf'
    }
    
    candidate_id = matcher.save_candidate(sample_candidate)
    print(f"Created candidate: {candidate_id}")
    
    # Find matches
    matches = matcher.find_matches(candidate_id)
    print(f"Found {len(matches)} matches")
    
    for match in matches[:3]:  # Show top 3 matches
        print(f"Job: {match['job_title']} - Score: {match['match_score']}%")

if __name__ == "__main__":
    main()
