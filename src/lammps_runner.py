# src/lammps_runner.py
"""
Runner LAMMPS – garante execução em modo **single‑process** (serial).

* binário encontrado via which (lmp ou lammps)
* sempre executado com `mpirun -np 1` → cria um rank MPI único
* flag `-sf none` desativa todas as acelerações (MPI, GPU, OpenMP)
* se `work_dir` for passado, o comando usa apenas o **nome** do script
  (para evitar caminhos como ``lammps/lammps/in.minimize``).
"""

import subprocess
from pathlib import Path
from typing import Tuple, Optional


def _find_executable() -> str:
    """Localiza o binário LAMMPS (lmp ou lammps) no PATH."""
    for exe in ("lmp", "lammps"):
        if subprocess.run(
            ["which", exe],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        ).returncode == 0:
            return exe
    raise FileNotFoundError(
        "Executável LAMMPS não encontrado no PATH. Instale LAMMPS ou "
        "adicione seu binário ao PATH."
    )


def run_lammps(
    input_path: Path,
    work_dir: Optional[Path] = None,
    *,
    capture_output: bool = True,
    timeout: Optional[int] = None,
) -> Tuple[Path, Path]:
    """
    Executa LAMMPS com o script de input fornecido.

    Parameters
    ----------
    input_path : Path
        Arquivo ``*.in`` contendo o comando LAMMPS.
    work_dir : Path, optional
        Diretório onde a execução ocorrerá (default = diretório do input).
    capture_output : bool, default True
        Captura stdout/stderr; levanta ``RuntimeError`` caso o retorno seja != 0.
    timeout : int, optional
        Tempo máximo em segundos; ``None`` → ilimitado.

    Returns
    -------
    Tuple[Path, Path]
        (log_path, dump_path) – caminhos absolutos dos artefatos
        gerados pelo input (log.lammps e dump.relaxed).
    """
    exe = _find_executable()

    # -----------------------------------------------------------------
    #  Construção do comando:
    #   mpirun -np 1 <exe> -sf none -in <script>
    #  Se work_dir for especificado, usamos apenas o nome do script
    #  (input_path.name) porque o cwd já está apontando para o diretório
    #  onde o arquivo está localizado.
    # -----------------------------------------------------------------
    script_arg = input_path.name if work_dir is not None else str(input_path)

    cmd = ["mpirun", "-np", "1", exe, "-sf", "none", "-in", script_arg]

    cwd = work_dir if work_dir is not None else input_path.parent

    result = subprocess.run(
        cmd,
        cwd=str(cwd),
        capture_output=capture_output,
        text=True,
        timeout=timeout,
    )

    # Se LAMMPS retornar código diferente de zero, levantamos erro.
    if result.returncode != 0:
        raise RuntimeError(
            f"LAMMPS terminou com código {result.returncode}. "
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )

    # -------------------------------------------------------------
    #  O input que criamos grava dois arquivos:
    #   * log.lammps
    #   * dump.relaxed
    # -------------------------------------------------------------
    log_path = Path(cwd) / "log.lammps"
    dump_path = Path(cwd) / "dump.relaxed"

    if not log_path.is_file():
        raise FileNotFoundError(f"Log LAMMPS esperado não encontrado: {log_path}")
    if not dump_path.is_file():
        raise FileNotFoundError(f"Dump LAMMPS esperado não encontrado: {dump_path}")

    return log_path.resolve(), dump_path.resolve()