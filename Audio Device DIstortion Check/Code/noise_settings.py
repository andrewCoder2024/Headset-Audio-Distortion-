import os


def get_noise_settings():
    # get names of files in directory
    for num, entry in enumerate(os.scandir('Noise')):
        if 'y' in input("Do you want to use this file?  \n    :: "
                        + os.path.splitext(entry.path)[0] + " ::"):
            return entry.path
        elif num == len([entry for entry in os.scandir('全局')]) - 1:
            return entry.path


get_noise_settings()
