# Apptainer for HADDOCK3 (MPI-Ready HPC)

This repository provides everything to build, run, and extend an **Apptainer** container for **HADDOCK3** with MPI support. **Apptainer** (formerly Singularity) is a container platform tailored for HPC environments — it enables reproducible, portable, and secure deployments without requiring root privileges, making it ideal for scientific workflows on clusters. **The biggest advantage** of Apptainer is that it seamlessly integrates with shared HPC filesystems and scheduler systems (e.g., SLURM, PBS) while preserving user permissions and security. [**HADDOCK3**](https://www.biorxiv.org/content/10.1101/2025.04.30.651432v1) is the latest version of the HADDOCK (High Ambiguity Driven protein–protein Docking) platform, a flexible, information-driven docking software suite for modeling biomolecular complexes using experimental and theoretical restraints.  
The container is fully backward-compatible with **Singularity**, so you can build and use the same definition file with either tool. Alongside HADDOCK3 itself, the container bundles essential editors, monitoring tools, file-sync utilities, and interactive environments (classic Jupyter Notebook & JupyterLab), plus utility scripts. You can easily customize the definition to include additional utilities or domain-specific tools when building your container image.

---

##  Repository Structure

```plaintext
├── apptainer_recipe/                  
│   └── HADDOCK3.def              # Apptainer/Singularity definition file
├── docs/                         # Documentation 
│   ├── usage.md                  # Usage guide
├── scripts/                      # Scripts
│   ├── slurm_run.sh              # Multi-node MPI run script
├── LICENSE                       # MIT License
├──  README.md                    # Overview
└── CONTRIBUTING.md               # Contribution guidelines
```

---

##  Quick Start

1. **Clone**

   ```bash
   git clone https://github.com/Comp-era/Apptainer-HADDOCK3.git
   cd Apptainer-Container-for-HADDOCK3/apptainer_reciepe
   ```

2. **Build** (Apptainer or Singularity)

   ```bash
   # Apptainer
   apptainer build haddock3_cpu-mpi.sif HADDOCK3.def

   # For Singularity
   singularity build haddock3_cpu-mpi.sif HADDOCK3.def
   ```

    **Tip:** To add more utilities or tools ( for custom tools or packages), simply modify the `%post` section of `HADDOCK3.def` before building.

3. **Download Pre-built Image**

   You can also pull the pre-built image directly from GitHub’s Container Registry using the ORAS protocol:

   ```bash
   apptainer pull oras://ghcr.io/comp-era/haddock3:2025.06-v1.0-haddock3-mpi
   ```

4. **Run**

   - **Shell**: interactive access
     ```bash
     apptainer shell haddock3_cpu-mpi.sif
     ```
   - **HADDOCK3**: verify installation
     ```bash
     apptainer exec haddock3_cpu-mpi.sif haddock3 --version
     ```

   Once verified, you can either:

Run locally on your system (for small test cases),

Or refer to the **usage.md** and the example SLURM script available in the scripts  folder for detailed instructions on how to run HADDOCK3 jobs in an HPC environment.

You can also run Jupyter Notebooks or JupyterLab inside the container for interactive sessions, analysis of outputs, data curation, or visualization of results. Make sure your $HOME directory contains the relevant input/output files and notebooks.

   - **Classic Notebook**:
     ```bash
     apptainer exec \
       --bind $HOME:$HOME \
       haddock3_cpu-mpi.sif \
       jupyter notebook \
         --ip=0.0.0.0 --no-browser --allow-root \
         --ServerApp.root_dir=$HOME/haddock3-mpi-container
     ```
   - **JupyterLab**:
     ```bash
     apptainer exec \
       --bind $HOME:$HOME \
       haddock3_cpu-mpi.sif \
       jupyter lab \
         --ip=0.0.0.0 --no-browser --allow-root \
         --ServerApp.root_dir=$HOME/haddock3-mpi-container
     ```

    **Note:** Some environments won’t auto-launch a browser. In that case:

   1. Copy the `http://127.0.0.1:8888/...` URL shown and paste it in your browser.
   2. Or run:
      ```bash
      xdg-open http://127.0.0.1:8888/?token=<your-token>
      ```

5. **Utilities & Editors** The container includes tools for development and debugging:

   - **Editors**: `vim`, `nano`, `emacs`
   - **Paging & Search**: `less`, `grep`, `ack`, `ripgrep`
   - **Process Monitoring**: `htop`, `ps`, `strace`, `lsof`
   - **Session Management**: `tmux`, `screen`
   - **File Sync**: `rsync`

---

##  Resources & Tutorials

- **Apptainer Installation & Usage**: Detailed installation instructions and usage examples can be found on the official docs: [apptainer.org/docs/admin/main/installation.html](https://apptainer.org/docs/admin/main/installation.html)
- **Official HADDOCK3 Tutorials**: Visit the Bonvin lab’s educational page for HADDOCK3 tutorials : [bonvinlab.org/education/HADDOCK3](https://www.bonvinlab.org/education/HADDOCK3/)
- **Source Code & Issues**: Explore the HADDOCK3 source code on GitHub: [github.com/haddocking/haddock3](https://github.com/haddocking/haddock3)

---

##  Requirements

- **Host**: Linux with Apptainer or Singularity installed (local machine or HPC environment)
- **Disk**: ≥ 2 GB free for building
- **Python**: 3.10+ (inside container)

---

##  Documentation

See the `docs/` folder:

- **usage.md** – Detailed uasge and tips

---

##  Contributing

Kindly refer to [CONTRIBUTING.md](CONTRIBUTING.md) , for contributions.



---

##  License

MIT License © 2025 Shantanu Khatri.

---

*Get ready for seamless HADDOCK3 runs, interactive analyses, and reproducible workflows!*

