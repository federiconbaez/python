
from typing import Optional
from core.contribution_generator import ContributionGenerator, ContributionGenerator
from interfaces.generator_interface import GeneratorInterface
import logging

# -----------------------------------------------------------------------------------------------------
# @ Generator Factory
# -----------------------------------------------------------------------------------------------------

class ContributionGeneratorFactory:
    """
    Factory class to create different types of contribution generators.
    """

    @staticmethod
    def create_generator(generator_type: str, repo_path: str, **kwargs) -> Optional[GeneratorInterface]:
        """
        Creates an instance of a contribution generator based on the specified type.

        Args:
            generator_type (str): The type of generator to create. Options are "simple" or "advanced".
            repo_path (str): The path to the repository where contributions are to be generated.
            **kwargs: Additional arguments to customize the generator behavior.

        Returns:
            ContributionGeneratorInterface: An instance of the requested contribution generator.
        """
        logging.info(f"Creating contribution generator of type: {generator_type}")
        try:
            if generator_type.lower() == "simple":
                return ContributionGenerator(repo_path, **kwargs)
            elif generator_type.lower() == "advanced":
                return ContributionGenerator(repo_path, **kwargs)
            else:
                logging.error(f"Unknown generator type: {generator_type}")
                return None
        except Exception as e:
            logging.error(f"Error creating generator of type '{generator_type}': {e}")
            raise

# -----------------------------------------------------------------------------------------------------
# @ Fin del Archivo Generator Factory
# -----------------------------------------------------------------------------------------------------
