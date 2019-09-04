// mx2Vision.cpp : This file contains the 'main' function. Program execution begins and ends there.


#include<iostream>
#include <opencv2/objdetect.hpp>
#include<opencv2/opencv.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
using namespace std;
using namespace cv;
int counter = 0;

void display(Mat &im, Mat &bbox)
{
	int n = bbox.rows;
	for (int i = 0; i < n; i++)
	{
		line(im, Point2i(bbox.at<float>(i, 0), bbox.at<float>(i, 1)), Point2i(bbox.at<float>((i + 1) % n, 0), bbox.at<float>((i + 1) % n, 1)), Scalar(255, 0, 0), 3);
		cout << bbox.at<float>(i, 0) + bbox.at<float>(i, 1);
	}
	
	imshow("Result", im);
}

int main(int argc, char** argv)
{
	VideoCapture cap(0); //open default camera --might need to change to work off webcam
	if (!cap.isOpened()) { //camera check
		cout << "Error opening camera" << endl;
		return -1;
	}


	while (1) {

		///////////////Camera Input///////////////////////////
		Mat frame;
		cap >> frame;

		if (frame.empty()) break;

		imshow("Frame", frame);

		char c = (char)waitKey(25);
		if (c == 27) break;		//If ESC is pressed then exit

		///////////////QR Code Detector////////////////////////

		//To detect orientation possibly add 2 qr codes and draw a vector between both
		QRCodeDetector qrDecoder = QRCodeDetector::QRCodeDetector();
		Mat bbox, rectifiedImage;
		std::string data = qrDecoder.detectAndDecode(frame, bbox, rectifiedImage);
		if (data.length() > 0) {
			cout << data << endl;
			//rectangle(frame, Point pt1, Point pt2, const Scalar& color, int thickness = 1, int lineType = 8, int shift = 0);
			display(frame, bbox);			//display() error doesn't work
			rectifiedImage.convertTo(rectifiedImage, CV_8UC3);
			//imshow("rectified QRCode", rectifiedImage); shows a separate image of the qr code
			//waitKey(0);		//need to remove then fix display() for bounding box
			//also need to make it detect from further distances
		}

	}

	cap.release();
	destroyAllWindows();
	return 0;
}
	/*
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
		//std::cout << "\n";
	}
	std::cout << counter;
	std::cout << "\n";
	

	imshow("detected circles", src);
	imshow("gray detected circles", gray);
	waitKey();
	return 0;
	*/


