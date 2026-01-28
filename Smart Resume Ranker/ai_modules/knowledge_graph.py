import random
import networkx as nx

class KnowledgeGraphMatcher:
    def __init__(self):
        # Mock Knowledge Graph connections
        self.related_skills = {
            'python': ['django', 'flask', 'pandas', 'numpy', 'scikit-learn'],
            'javascript': ['react', 'node', 'vue', 'angular', 'typescript'],
            'data': ['sql', 'analysis', 'visualization', 'tableau', 'powerbi']
        }
        self.graph = nx.Graph()
        self._build_knowledge_graph()

    def _build_knowledge_graph(self):
        """
        Builds a knowledge graph of related skills.
        """
        skills = {
            'python': ['django', 'flask', 'pandas', 'numpy', 'scikit-learn'],
            'javascript': ['react', 'node', 'vue', 'angular', 'typescript'],
            'data': ['sql', 'analysis', 'visualization', 'tableau', 'powerbi']
        }
        for main_skill, related_skills in skills.items():
            self.graph.add_node(main_skill, type='skill')
            for related_skill in related_skills:
                self.graph.add_node(related_skill, type='skill')
                self.graph.add_edge(main_skill, related_skill)

    def graph_similarity(self, job_desc, resume_text):
        """
        Calculates similarity based on skill relationships in the knowledge graph.
        """
        job_skills = self._extract_skills(job_desc)
        resume_skills = self._extract_skills(resume_text)
        
        if not job_skills or not resume_skills:
            return 0.0
        
        total_similarity = 0
        for job_skill in job_skills:
            for resume_skill in resume_skills:
                if self.graph.has_node(job_skill) and self.graph.has_node(resume_skill):
                    try:
                        path_length = nx.shortest_path_length(self.graph, source=job_skill, target=resume_skill)
                        total_similarity += 1 / (1 + path_length)
                    except nx.NetworkXNoPath:
                        continue
        
        return min(total_similarity * 20, 100.0)

    def _extract_skills(self, text):
        """
        Extracts skills from text based on the knowledge graph nodes.
        """
        return {node for node in self.graph.nodes if node in text.lower()}
