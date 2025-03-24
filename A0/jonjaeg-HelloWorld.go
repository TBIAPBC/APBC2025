package main

import (
	"fmt"
	"io"
	"os"
)

func main() {
	// Check for command-line arguments
	if len(os.Args) < 2 {
		fmt.Println("Usage: go run main.go <input_file>")
		return
	}

	inputFileName := os.Args[1]
	outputFileName := "output.txt"

	// Read the input file
	inputFile, err := os.Open(inputFileName)
	if err != nil {
		fmt.Println("Error reading input file:", err)
		return
	}
	defer inputFile.Close()

	inputData, err := io.ReadAll(inputFile)
	if err != nil {
		fmt.Println("Error reading file content:", err)
		return
	}

	// Prepare the output content
	outputData := []byte("Hello World!\n" + string(inputData))

	// Write to the output file
	err = os.WriteFile(outputFileName, outputData, 0644)
	if err != nil {
		fmt.Println("Error writing output file:", err)
		return
	}

	fmt.Println("File written successfully to", outputFileName)
}
