"""Set of functionalities to run prodigy-ligand.

DevNotes:
The magic happens in haddock.libs.libprodigy
"""

from haddock.core.typing import FilePath, ParamDict
from haddock.libs.libontology import PDBFile
from haddock.libs.libprodigy import ProdigyBaseJob, ProdigyWorker


class ProdigyLigand(ProdigyWorker):
    """Class managing the computation of protein-ligand with prodigy."""

    def __init__(self, model: FilePath, params: ParamDict) -> None:
        """Instantiate the class with superclass."""
        super().__init__(model, params)
        self.receptor_chain = self.params["receptor_chain"]
        self.lig_resname = self.params["ligand_resname"]
        self.lig_chain = self.params["ligand_chain"]

    def evaluate_complex(self) -> float:
        """Evaluate a complex with prodigy-lig.

        Returns
        -------
        deltaG : float
            The computed DeltaG of the input complex.
        """
        from prodigy_lig.prodigy_lig import (
            basename,
            extract_electrostatics,
            FastMMCIFParser,
            PDBParser,
            ProdigyLig,
            splitext,
            )
        # Mimic prodigy-ligand main
        fname, s_ext = splitext(basename(self.model))
        if s_ext in (".pdb", ".ent", ):
            parser = PDBParser(QUIET=1)
        elif s_ext == ".cif":
            parser = FastMMCIFParser(QUIET=1)

        with open(self.model) as in_file:
            # try to set electrostatics from input file if not provided by user
            electrostatics = False
            try:
                electrostatics = extract_electrostatics(in_file)
            except Exception:
                pass
            prodigy_lig = ProdigyLig(
                parser.get_structure(fname, in_file),
                chains=[
                    f"{self.receptor_chain}:{self.lig_chain}",
                    f"{self.lig_chain}:{self.lig_resname}",
                    ],
                electrostatics=electrostatics,
                cutoff=self.dist_cutoff,
                )
        # Run predictions
        prodigy_lig.predict()
        # Retrieve DeltaG
        deltaG = prodigy_lig.dg_elec if prodigy_lig.dg_elec else prodigy_lig.dg
        return deltaG


class ProdigyJob(ProdigyBaseJob):
    """Managing the computation of prodigy scores within haddock3."""

    def __init__(
            self,
            model: PDBFile,
            params: ParamDict,
            index: int = 1,
            ) -> None:
        """Instantiate the class with superclass."""
        super().__init__(model, params, index)
    
    @staticmethod
    def get_worker() -> object:
        """Return the appropriate worker."""
        return ProdigyLigand
