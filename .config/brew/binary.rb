class Latestos < Formula
  desc "A Python CLI that acquires direct links to operating system&#x27;s ISO installers"
  homepage "https://megabyte.space"
  url "https://github.com/megabyte-labs/latestos/releases/download/v0.0.1/latestos.tar.gz"
  version "0.0.1"
  license "MIT"

  

  def install
    os = OS.kernel_name.downcase
    arch = Hardware::CPU.intel? ? "amd64" : Hardware::CPU.arch.to_s
    bin.install "build/bin/latestos-#{os}_#{arch}" => "latestos"
  done

  test do
    system bin/"latestos", "--version"
  end
end
