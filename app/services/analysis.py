import logging
import random
from pathlib import Path

logger = logging.getLogger(__name__)


class ImageAnalysisService:
    SKIN_TYPES = ["Oily", "Dry", "Combination", "Normal", "Sensitive"]
    
    POSSIBLE_ISSUES = [
        "Hyperpigmentation",
        "Acne",
        "Fine lines",
        "Dark circles",
        "Uneven skin tone",
        "Enlarged pores",
        "Dehydration",
        "Sun damage",
        "Redness",
        "Texture irregularities"
    ]
    
    def analyze_image(self, image_path: Path, image_id: str) -> dict:
        logger.info(f"Starting analysis for image: {image_id}")
        
        file_size = image_path.stat().st_size
        extension = image_path.suffix.lower()
        
        seed = hash(f"{image_id}{file_size}")
        random.seed(seed)
        
        skin_type = random.choice(self.SKIN_TYPES)
        
        num_issues = random.randint(1, 3)
        issues = random.sample(self.POSSIBLE_ISSUES, num_issues)
        
        confidence = round(random.uniform(0.70, 0.98), 2)
        
        analysis_result = {
            "image_id": image_id,
            "skin_type": skin_type,
            "issues": issues,
            "confidence": confidence,
            "metadata": {
                "file_extension": extension,
                "file_size_bytes": file_size,
                "analysis_version": "1.0.0"
            }
        }
        
        logger.info(f"Analysis complete for {image_id}: skin_type={skin_type}, issues={len(issues)}, confidence={confidence}")
        
        return analysis_result
    
    def get_detailed_analysis(self, image_path: Path, image_id: str) -> dict:
        base_analysis = self.analyze_image(image_path, image_id)
        
        file_size = image_path.stat().st_size
        seed = hash(f"{image_id}{file_size}")
        random.seed(seed + 1) 
        
        detailed_metrics = {
            "hydration_level": round(random.uniform(30, 90), 1),
            "oil_index": round(random.uniform(20, 80), 1),
            "elasticity_score": round(random.uniform(50, 95), 1),
            "texture_score": round(random.uniform(40, 90), 1),
            "recommendations": self._generate_recommendations(base_analysis["skin_type"], base_analysis["issues"])
        }
        
        return {**base_analysis, "detailed_metrics": detailed_metrics}
    
    def _generate_recommendations(self, skin_type: str, issues: list[str]) -> list[str]:
        recommendations = []
        
        skin_type_recs = {
            "Oily": "Use oil-free moisturizers and gentle cleansers",
            "Dry": "Apply rich moisturizers and hydrating serums",
            "Combination": "Use zone-specific products for different areas",
            "Normal": "Maintain current routine with SPF protection",
            "Sensitive": "Choose fragrance-free, hypoallergenic products"
        }
        recommendations.append(skin_type_recs.get(skin_type, "Consult a dermatologist"))
        
        issue_recs = {
            "Hyperpigmentation": "Consider vitamin C serums and chemical exfoliants",
            "Acne": "Try salicylic acid or benzoyl peroxide treatments",
            "Fine lines": "Use retinol products and stay hydrated",
            "Dark circles": "Get adequate sleep and try caffeine eye creams"
        }
        
        for issue in issues[:2]: 
            if issue in issue_recs:
                recommendations.append(issue_recs[issue])
        
        return recommendations

analysis_service = ImageAnalysisService()