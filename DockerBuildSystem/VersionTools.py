from DockerBuildSystem import TerminalTools

def ExportVersionFromChangelogToEnvironment(changelogFile, versionName):
    version = GetVersionFromChangelog(changelogFile)
    TerminalTools.ExportVariableToEnvironment(version, versionName)

def GetVersionFromChangelog(changelogFile):
    with open(changelogFile) as f:
        lines = f.readlines()
    for line in lines:
        splitLine = line.split()
        if len(splitLine) < 4:
            continue
        if splitLine[0] == "###" and splitLine[1].upper() == "VERSION":
            version = splitLine[2].replace(",", "")
            return version
    raise Exception("No version found in changelog file: " + str(changelogFile))



