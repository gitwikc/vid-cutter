import os
import click
import subprocess
import tqdm


class ProgressBar:
    def __init__(self, total):
        self.total = total
        self.current = 0

    def update(self):
        self.current += 1
        click.echo(f"Progress: {self.current}/{self.total}")

    def finish(self):
        click.echo("Done!")


@click.command()
@click.option(
    "--input_folder_path",
    "-i",
    help="The input folder",
    prompt="Enter the path to the input folder",
)
@click.option(
    "--output_folder_path",
    "-o",
    help="The output folder",
    prompt="Enter the path to the output folder",
)
def main(input_folder_path, output_folder_path):
    """
    Reads in all videos inside a folder and uses ffmpeg to create a new video titled {filename}_5sec.mp4
    inside the cuts-5sec folder.
    """

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # Get a list of all files in the input folder
    input_files = os.listdir(input_folder_path)

    # Create a progress bar
    progress_bar = ProgressBar(len(input_files))

    # Iterate over the input files and create a new video for each one
    for input_file in input_files:
        # Get the path to the input file
        input_file_path = os.path.join(input_folder_path, input_file)

        # Get the filename without the extension
        filename = os.path.splitext(input_file)[0]

        # Create the output file path
        output_file_path = os.path.join(
            output_folder_path, f"{filename}_5sec.mp4")

        # Create the output video using ffmpeg
        subprocess.run(
            [
                "ffmpeg",
                "-hide_banner",
                "-loglevel",
                "quiet",
                "-i",
                input_file_path,
                "-t",
                "5",
                "-c:v",
                "copy",
                "-c:a",
                "copy",
                output_file_path,
            ]
        )

        # Update the progress bar
        progress_bar.update()

    # Finish the progress bar
    progress_bar.finish()


if __name__ == "__main__":
    main()
