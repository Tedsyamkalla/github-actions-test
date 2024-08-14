import dagger
from dagger import dag, function, object_type
import os

@object_type
class Midas:
    @function
    def container(self) -> dagger.Container:
        """Set up container"""
        return (
            dag.container().from_(
                "asia-southeast2-docker.pkg.dev/cf-data-engineering/dataplatform/testing-dbt-teddy:latest"
            )
        )
    
    @function
    async def dbt_run(self) -> str:
        """Run dbt for a specific model"""
        model_name = os.getenv("MODEL_NAME", "")
        is_full_refresh = os.getenv("IS_FULL_REFRESH", "true").lower() == "true"
        profile = os.getenv("PROFILE", "production")
        
        dbt_argument = [
            "--profiles-dir", f"./profiles/{profile}/",
            "--target", "production"
        ]
        
        dbt_run_command = [
            "dbt", "--cache-selected-only", "run"
        ] + dbt_argument + ["--select", model_name]
        
        if is_full_refresh:
            dbt_run_command.append("--full-refresh")

        container = self.container()
        run = await container.with_exec(dbt_run_command).stdout()

        return run
