from DockerBuildSystem import TerminalTools

def ExportVersionFromChangelogToEnvironment(changelogFile, versionName):
    version = GetVersionFromChangelog(changelogFile)
    TerminalTools.ExportVariableToEnvironment(version, versionName)

def GetVersionFromChangelog(changelogFile):
    with open(changelogFile) as f:
        lines = f.readlines()
    for line in lines:
        splitLine = line.split()
        if len(splitLine) == 0:
            continue

        # General criterias
        if not(splitLine[0] == "##" or splitLine[0] == "###"):
            continue

        # Changelog version 1
        if len(splitLine) >= 3 and splitLine[1].upper() == "VERSION":
            version = splitLine[2].replace(",", "")
            return version

        # Changelog version 2
        elif len(splitLine) >= 2 and splitLine[1][0] == '[' and splitLine[1][-1] == ']':
            version = splitLine[1][1:-1].replace(",", "").replace(" ", "")
            return version

    raise Exception("No version found in changelog file: " + str(changelogFile))
        
    

