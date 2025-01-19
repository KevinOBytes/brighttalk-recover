"""Progress monitoring utilities."""

from tqdm import tqdm


class DownloadProgress:
    """Handles download progress monitoring."""

    def __init__(self, total_bytes: int, desc: str = "Downloading") -> None:
        self.pbar = tqdm(
            total=total_bytes,
            desc=desc,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        )

    def update(self, chunk_size: int) -> None:
        """Update progress bar with chunk size."""
        self.pbar.update(chunk_size)

    def close(self) -> None:
        """Close progress bar."""
        self.pbar.close()
