#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import subprocess
import signal


class VideoStreamer(Node):
    def __init__(self):
        super().__init__('video_streamer')

        # Comando ffmpeg que deseas ejecutar
        self.ffmpeg_cmd = [
            'ffmpeg',
            '-f', 'v4l2',
            '-i', '/dev/video2',
            '-vcodec', 'mpeg1video',
            '-f', 'mpegts',
            'udp://127.0.0.1:1235'
        ]

        self.get_logger().info("Iniciando transmisión UDP desde /dev/video2 ...")

        # Lanzar proceso ffmpeg
        try:
            self.process = subprocess.Popen(self.ffmpeg_cmd)
            self.get_logger().info("ffmpeg iniciado correctamente.")
        except Exception as e:
            self.get_logger().error(f"Error al iniciar ffmpeg: {e}")

        # Timer para vigilar el proceso
        self.create_timer(2.0, self.check_process)

    def check_process(self):
        """Verifica si ffmpeg sigue vivo."""
        if self.process.poll() is not None:
            self.get_logger().error("El proceso ffmpeg se detuvo.")
        else:
            self.get_logger().debug("ffmpeg está corriendo...")


    def destroy_node(self):
        """Detiene ffmpeg al cerrar el nodo."""
        self.get_logger().info("Cerrando ffmpeg...")
        try:
            self.process.send_signal(signal.SIGINT)
            self.process.wait()
        except Exception:
            pass
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = VideoStreamer()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
