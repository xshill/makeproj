#!/usr/bin/env python
import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a file structure for a project using Make")
    parser.add_argument("directory", help="the directory for the project", nargs=1)
    parser.add_argument("--cpp", help="use g++", action="store_const", const="g++", default="gcc", dest="compiler")
    parser.add_argument("-n", "--name", help="the executable name (default: directory name)")
    parser.add_argument("-e", "--extension", help="the file extension for source files")
    parser.add_argument("-v", "--verbose", help="output all generated files", action="store_const", const=True, default=False)
    parser.add_argument("--gitignore", help="generate .gitignore file", action="store_const", const=True, default=False)

    args = parser.parse_args()

    try:
        directory = os.path.abspath(args.directory[0])
        dirname = os.path.basename(os.path.dirname(directory + "/"))
        os.mkdir(directory)
        if args.verbose: print("Directory " + directory + " created")
        os.mkdir(directory + "/include")
        if args.verbose: print("Directory " + directory + "/include created")
        os.mkdir(directory + "/src")
        if args.verbose: print("Directory " + directory + "/src created")

        if args.name is None:
            args.name = dirname

        if args.extension is None:
            if args.compiler == "gcc":
                args.extension = "c"
            elif args.compiler == "g++":
                args.extension = "cpp"

        if " " in args.extension:
            raise Exception("The file extension should not contain spaces")

        with open(directory + "/Makefile", "w") as f:
            f.write("CC = " + args.compiler + "\n")
            f.write("FILENAME = " + args.name + "\n")
            f.write("OBJS = \n")
            f.write("CFLAGS = -Iinclude\n\n")
            f.write("main: bin build $(OBJS)\n")
            f.write("\t$(CC) -o bin/$(FILENAME) $(OBJS) $(CFLAGS)\n\n")
            f.write("bin:\n\tmkdir -p bin\n\n")
            f.write("build:\n\tmkdir -p build\n\n")
            f.write("build/%.o: src/%." + args.extension + "\n\t$(CC) -c -o $@ $< $(CFLAGS)\n\n")
            f.write("clean:\n\trm bin/$(FILENAME)\n\trm build/*.o\n")

        if args.verbose: print("File " + directory + "/Makefile created")

        if args.gitignore:
            with open(directory + "/.gitignore", "w") as f:
                f.write("bin/\n")
                f.write("build/\n")

            if args.verbose: print("File " + directory + "/.gitignore created")

        print("Project " + args.directory[0] + " created!")
    except Exception as e:
        print(e)
