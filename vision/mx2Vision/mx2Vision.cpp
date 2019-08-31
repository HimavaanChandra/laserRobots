// mx2Vision.cpp : This file contains the 'main' function. Program execution begins and ends there.
#include<opencv2/opencv.hpp>
#include<iostream>
using namespace std;
using namespace cv;
int counter = 0;

int main(int argc, char** argv)
{
	const char* filename = argc >= 2 ? argv[1] : "colourBalls.jpg";
	
	Mat src = imread(filename, IMREAD_COLOR); // Loads an image
	Mat srcg = imread(filename, IMREAD_GRAYSCALE); // Loads an image
	
	if (src.empty()) { // Check if image is loaded fine
		printf(" Error opening image\n");
		printf(" Program Arguments: [image_name -- default %s] \n", filename);
		return -1;
	}

	Mat gray;
	cvtColor(src, gray, COLOR_BGR2GRAY);

	medianBlur(gray, gray, 7);

	vector<Vec3f> circles;
	HoughCircles(gray, circles, HOUGH_GRADIENT, 1,
		gray.rows / 30, // change this value to detect circles with different distances to each other default:16
		100, 30, 15, 200	// change the last two parameters
						// (min_radius & max_radius) to detect larger circles
	);

	for (size_t i = 0; i < circles.size(); i++)
	{
		Vec3i c = circles[i];
		Point center = Point(c[0], c[1]);
		// circle center
		circle(src, center, 1, Scalar(0, 100, 100), 3, LINE_AA);
		// circle outline
		int radius = c[2];
		circle(src, center, radius, Scalar(255, 0, 255), 3, LINE_AA);
		counter++;		//keep track of number of circles
		//std::cout << src(center);
		std::cout << "\n";
	}
	std::cout << counter;
	std::cout << "\n";
	

	imshow("detected circles", src);
	//imshow("gray detected circles", srcg);
	waitKey();
	return 0;
}
 
//std::cout << "Hello World!\n"; 


