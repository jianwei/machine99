sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.9 python3.9-dev

sudo apt install curl -y
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.9 get-pip.py
export PATH=/home/coolpi/.local/bin:$PATH
pip3 -V
pip3 install numpy --upgrade
pip3 install opencv-python
#check opencv
python3.9 -c "import cv2; print(cv2.__version__)"


git clone https://gitee.com/yanyitech/rknpu2.git
sudo cp -arf rknpu2/runtime/RK3588/Linux/librknn_api/aarch64/* /usr/lib/
git clone https://gitee.com/yanyitech/rknn-toolkit2.git
pip3 install rknn-toolkit2/rknn_toolkit_lite2/packages/rknn_toolkit_lite2-1.4.0-cp39-cp39-linux_aarch64.whl

cd rknn-toolkit2/rknn_toolkit_lite2/examples/inference_with_lite
python3.9 test.py
