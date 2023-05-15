if [ ! -f "./Stockfish/src/stockfish" ]; then
    cd Stockfish/src; make -j build ARCH=x86-64-modern; cd ../..
fi

#rm -rf build; mkdir build; cd build; cmake ..; make all; cd ..
