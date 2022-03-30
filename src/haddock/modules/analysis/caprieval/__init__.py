"""Calculate CAPRI metrics."""
from pathlib import Path

from haddock.libs.libontology import ModuleIO
from haddock.modules import BaseHaddockModule
from haddock.modules.analysis.caprieval.capri import CAPRI
# for parallelisation
from haddock.libs.libsubprocess import CapriJob
from haddock.libs.libparallel import Scheduler
from haddock import log

RECIPE_PATH = Path(__file__).resolve().parent
DEFAULT_CONFIG = Path(RECIPE_PATH, "defaults.yaml")

class HaddockModule(BaseHaddockModule):
    """HADDOCK3 module to calculate the CAPRI metrics."""

    name = RECIPE_PATH.name

    def __init__(self, order, path, *ignore, init_params=DEFAULT_CONFIG,
                 **everything):
        super().__init__(order, path, init_params)

    @classmethod
    def confirm_installation(cls):
        """Confirm if contact executable is compiled."""
        return

    def rearrange_output_files(self, output_name, capri_path):
        """function to combine different capri outputs in a single file"""
        output_fname = Path(capri_path,output_name)
        self.log(f"rearranging output files into {output_fname}")
        keyword = output_name.split(".")[0]
        split_dict = {"capri_ss" : "model-cluster-ranking", "capri_clt" : "caprieval_rank"}
        if keyword not in split_dict.keys():
            raise Exception(f'Keyword {keyword} does not exist.')
        # Combine files
        with open(output_fname, 'w') as out_file:
            for core in range(self.params['ncores']):
                tmp_file = Path(capri_path, keyword + "_" + str(core) + ".tsv")
                with open(tmp_file) as infile:
                    if core == 0:
                        out_file.write(infile.read().rstrip("\n"))
                    else:
                        out_file.write(infile.read().split(split_dict[keyword])[1].rstrip("\n"))
                self.log(f"File number {core} written")
        self.log(f"Completed reconstruction of caprieval files. {output_fname} created")

    def _run(self):
        """Execute module."""
        # Get the models generated in previous step
        if type(self.previous_io) == iter:
            _e = "This module cannot come after one that produced an iterable."
            self.finish_with_error(_e)

        models_to_calc = self.previous_io.retrieve_models()

        #  Sort by score
        models_to_calc.sort()
        best_model_fname = Path(models_to_calc[0].rel_path)
        if self.params["reference_fname"]:
            reference = Path(self.params["reference_fname"])
        else:
            self.log(
                "No reference was given. "
                "Using the structure with the lowest score from previous step")
            reference = best_model_fname

        # Parallelisation : optimal dispatching of models
        nmodels = len(models_to_calc)
        base_models = nmodels//self.params['ncores']
        modulo = nmodels%self.params['ncores']
        chain_of_idx = [0]
        for core in range(self.params['ncores']):
            if core < modulo:
                chain_of_idx.append(chain_of_idx[core]+base_models+1)
            else:
                chain_of_idx.append(chain_of_idx[core]+base_models)
        # Starting jobs
        capri_jobs = []
        cluster_info = []
        self.log(f"running Capri Jobs in parallel with {self.params['ncores']} cores")
        for core in range(self.params['ncores']):
            # init Capri
            capri_obj = CAPRI(
            reference,
            models_to_calc[chain_of_idx[core]:chain_of_idx[core+1]],
            receptor_chain=self.params["receptor_chain"],
            ligand_chain=self.params["ligand_chain"],
            aln_method=self.params["alignment_method"],
            path=Path("."),
            lovoalign_exec=self.params["lovoalign_exec"],
            core=core,
            core_model_idx = chain_of_idx[core]
            )
            # Name job
            job_f = Path("capri_ss_" + str(core) + ".tsv")
            # Get cluster info
            cluster_info.append(any(m.clt_id for m in capri_obj.model_list))
            # init CapriJob
            job = CapriJob(
                job_f,
                self.params,
                capri_obj
                )
            capri_jobs.append(job)
        # Running parallel Capri Jobs
        capri_engine = Scheduler(capri_jobs, ncores=self.params['ncores'])
        capri_engine.run()
        # Check correct execution of parallel Capri Jobs
        capri_file_l = []
        not_found = []
        for job in capri_jobs:
            if not job.output.exists():
                not_found.append(job.input.name)
                log.warning(f'Capri results were not calculated for {job.input.name}')
            else:
                capri_file_l.append(str(job.output))
        if not_found:
            # Not all capri objects were calculated
            self.finish_with_error("Several capri files were not generated:"
                                   f" {not_found}")
        # Post-processing : single structure
        self.rearrange_output_files(output_name="capri_ss.tsv", capri_path=capri_obj.path)
        # Post-processing : clusters
        has_cluster_info = any(cluster_info)
        if not has_cluster_info:
            self.log("No cluster information")
        else:
            self.rearrange_output_files(output_name="capri_clt.tsv", capri_path=capri_obj.path)
        # Sending models to the next step of the workflow
        selected_models = models_to_calc
        io = ModuleIO()
        io.add(selected_models, "o")
        io.save()