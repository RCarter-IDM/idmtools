from examples.ssmt.simple_analysis.analyzers.AdultVectorsAnalyzer import AdultVectorsAnalyzer
from examples.ssmt.simple_analysis.analyzers.PopulationAnalyzer import PopulationAnalyzer
from idmtools.core.platform_factory import Platform
from idmtools.analysis.platform_anaylsis import PlatformAnalysis

if __name__ == "__main__":
    platform = Platform('SSMT')
    analysis = PlatformAnalysis(platform=platform,
                                experiment_ids=["8bb8ae8f-793c-ea11-a2be-f0921c167861"],
                                analyzers=[PopulationAnalyzer, AdultVectorsAnalyzer],
                                analyzers_args=[{'title': 'idm'}, {'name': 'global good'}],
                                analysis_name="SSMT Analysis Simple 1")

    analysis.analyze(check_status=True)
    wi = analysis.get_work_item()
    print(wi)