// mx2Vision.cpp : This file contains the 'main' function. Program execution begins and ends there.
#include<opencv2/opencv.hpp>
#include<iostream>
using namespace std;
using namespace cv;

int main(int argv, char** argc)
{
	Mat img = imread("lena.jpg");
	namedWindow("image", WINDOW_NORMAL);
	imshow("image", img);
	waitKey(0);
	return 0;
}
 
//std::cout << "Hello World!\n"; 


