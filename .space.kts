job("Build, publish") {
    container(image = "python_custom_img:0.0.1") {
        // specify URL of the package index using env var
        env["URL"] = "https://pypi.pkg.jetbrains.space/ikit-ki20-161-b/p/team-course-project-2022-2023/python/simple"

        // We suppose that your project has default build configuration -
        // the built package is saved to the ./dist directory
        shellScript {
            content = """
                echo Install requirements...
                pip install rich invoke
                echo Build project...
                inv docker.clear
                inv docker.build
                inv docker.run_background
                echo Upload package...
                twine upload --repository-url ${'$'}URL -u ${'$'}JB_SPACE_CLIENT_ID -p ${'$'}JB_SPACE_CLIENT_SECRET dist/*
            """
        }
    }
}